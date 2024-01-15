import ast
import os
import json
import yaml
import hashlib
import pickle
from pathlib import Path
from collections import defaultdict
from typing import Dict, Set, Any, Optional, List, Tuple
import concurrent.futures
import asyncio
import time
import gc
import psutil
from functools import lru_cache

from .config import DEFAULT_CONFIG, SeppyConfig, CACHE_DIR_NAME
from .models import ModuleInfo, CacheData, ProcessingStats
from .exceptions import ParseError, ModuleProcessingError, CacheError
from .utils import time_operation, logger
from .analyzers import (
    find_used_imports,
    find_used_globals,
    extract_imports,
    analyze_complex_structures,
    get_parent_function_or_class,
    is_node_in_function_or_class
)
from .processors import (
    organize_imports,
    create_module_code,
    create_module_docs,
    create_complex_module
)

class Seppy:
    def __init__(
        self,
        source_file: str,
        config_file: Optional[str] = None,
        memory_limit_mb: Optional[int] = None
    ):
        """Initialize Seppy with configuration.
        
        Args:
            source_file: Path to the source Python file
            config_file: Optional path to configuration file
            memory_limit_mb: Optional memory limit override
        """
        self.source_file = source_file
        self.config = self._load_config(config_file)
        
        # Override memory limit if provided
        if memory_limit_mb is not None:
            self.config["MEMORY_LIMIT_MB"] = memory_limit_mb
        
        self.modules: Dict[str, ModuleInfo] = {}
        self.dependencies_graph: Dict[str, Set[str]] = defaultdict(set)
        self.type_annotations: Dict[str, str] = {}
        self.has_async_code = False
        self.cache_dir = Path(CACHE_DIR_NAME)
        
        if self.config["CACHE_ENABLED"]:
            self.cache_dir.mkdir(exist_ok=True)
        
        self.stats = ProcessingStats()
        self.memory_limit = self.config["MEMORY_LIMIT_MB"] * 1024 * 1024
        self.performance_stats = {
            'start_time': time.time(),
            'memory_usage': [],
            'processing_times': defaultdict(list)
        }
    
        # Configure logging
        logger.setLevel(self.config["LOG_LEVEL"])
        logger.info(f"Initialized Seppy with config: {self.config}")

    def _load_config(self, config_file: Optional[str]) -> SeppyConfig:
        """Load configuration from file or use defaults."""
        config = DEFAULT_CONFIG.copy()
        
        if config_file:
            try:
                with open(config_file) as f:
                    if config_file.endswith('.json'):
                        user_config = json.load(f)
                    elif config_file.endswith('.yaml') or config_file.endswith('.yml'):
                        user_config = yaml.safe_load(f)
                    else:
                        raise ValueError("Config file must be .json or .yaml")
                    
                config.update(user_config)
                logger.info(f"Loaded configuration from {config_file}")
            except Exception as e:
                logger.warning(f"Failed to load config file: {e}. Using defaults.")
        
        return config

    @time_operation("parse_script")
    def parse_script(self, source_file: str) -> Dict[str, ModuleInfo]:
        """Parse Python script and extract module information."""
        try:
            with open(source_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            self._analyze_dependencies(tree)
            
            # Extract global variables and imports
            global_vars = set()
            imports = extract_imports(tree)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
                    if not is_node_in_function_or_class(node, tree):
                        global_vars.add(node.id)
            
            # Split into modules
            functions = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
            async_functions = [n for n in ast.walk(tree) if isinstance(n, ast.AsyncFunctionDef)]
            classes = [n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]
            
            if async_functions:
                self.has_async_code = True
            
            # Store modules in instance variable
            self.modules = self._split_into_modules(tree, global_vars, functions, async_functions, classes)
            
            self.stats.total_modules = len(self.modules)
            return self.modules
            
        except Exception as e:
            raise ParseError(f"Failed to parse script: {str(e)}")

    def _analyze_dependencies(self, tree: ast.AST) -> None:
        """Analyze dependencies between different parts of the code."""
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                parent = get_parent_function_or_class(node, tree)
                if parent:
                    self.dependencies_graph[parent].add(node.name)
                
                # Analyze function calls and attribute access
                for child in ast.walk(node):
                    if isinstance(child, ast.Call):
                        if isinstance(child.func, ast.Name):
                            self.dependencies_graph[node.name].add(child.func.id)
                        elif isinstance(child.func, ast.Attribute):
                            if isinstance(child.func.value, ast.Name):
                                self.dependencies_graph[node.name].add(child.func.value.id)

    def _split_into_modules(
        self,
        tree: ast.AST,
        global_vars: Dict[str, Any],
        functions: List[ast.FunctionDef],
        async_functions: List[ast.AsyncFunctionDef],
        classes: List[ast.ClassDef]
    ) -> Dict[str, ModuleInfo]:
        """Split code into separate modules."""
        modules = {}
        
        # Get source code
        try:
            with open(self.source_file, 'r', encoding='utf-8') as f:
                source_code = f.read()
        except Exception as e:
            logger.warning(f"Could not read source file for code preservation: {e}")
            source_code = ""
        
        # Create module for each class
        for class_node in classes:
            class_name = class_node.name.lower()
            if not any(class_name.startswith(prefix) for prefix in self.config["IGNORE_PATTERNS"]):
                structures = analyze_complex_structures(class_node, source_code)
                code = create_complex_module(class_name, class_node, structures)
                
                modules[class_name] = ModuleInfo(
                    name=class_name,
                    code=code,
                    imports=structures['imports'],
                    global_vars=structures['globals'],
                    functions=set(structures['functions'].keys()),
                    classes=set(structures['classes'].keys()),
                    docstring=ast.get_docstring(class_node)
                )
        
        # Create module for each function
        for func_node in functions + async_functions:
            func_name = func_node.name.lower()
            if not any(func_name.startswith(prefix) for prefix in self.config["IGNORE_PATTERNS"]):
                structures = analyze_complex_structures(func_node, source_code)
                code = create_complex_module(func_name, func_node, structures)
                
                modules[func_name] = ModuleInfo(
                    name=func_name,
                    code=code,
                    imports=structures['imports'],
                    global_vars=structures['globals'],
                    functions={func_node.name},
                    classes=set(),
                    async_functions={func_node.name} if isinstance(func_node, ast.AsyncFunctionDef) else set(),
                    docstring=ast.get_docstring(func_node)
                )
        
        return modules

    def save_modules(self, output_dir: str):
        """Save split modules to files."""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Save each module
        for name, module in self.modules.items():
            module_path = output_path / f"{name}.py"
            try:
                with open(module_path, 'w', encoding='utf-8') as f:
                    f.write(module.code)
                logger.info(f"Saved module {name} to {module_path}")
            except Exception as e:
                logger.error(f"Failed to save module {name}: {str(e)}")
        
        # Generate and save documentation
        docs_path = output_path / "docs"
        docs_path.mkdir(exist_ok=True)
        
        for name, module in self.modules.items():
            doc_path = docs_path / f"{name}.md"
            try:
                docs = create_module_docs(name, module.code)
                with open(doc_path, 'w', encoding='utf-8') as f:
                    f.write(docs)
                logger.info(f"Saved documentation for {name} to {doc_path}")
            except Exception as e:
                logger.error(f"Failed to save documentation for {name}: {str(e)}")
        
        # Save dependency graph
        try:
            # Convert sets to lists for JSON serialization
            serializable_graph = {k: list(v) for k, v in self.dependencies_graph.items()}
            graph_path = output_path / "dependencies.json"
            with open(graph_path, 'w', encoding='utf-8') as f:
                json.dump(serializable_graph, f, indent=2)
            logger.info(f"Saved dependency graph to {graph_path}")
        except Exception as e:
            logger.error(f"Failed to save dependency graph: {str(e)}")

    def _generate_performance_report(self) -> str:
        """Generate a performance report."""
        end_time = time.time()
        total_time = end_time - self.performance_stats['start_time']
        
        report = [
            "# Performance Report",
            f"\nTotal processing time: {total_time:.2f} seconds",
            f"\nModules processed: {self.stats.processed_modules}",
            f"Cached modules: {self.stats.cached_modules}",
            f"Failed modules: {self.stats.failed_modules}",
            "\nMemory Usage:",
            f"Peak: {max(self.performance_stats['memory_usage'])} MB",
            f"Average: {sum(self.performance_stats['memory_usage']) / len(self.performance_stats['memory_usage']):.2f} MB"
        ]
        
        return "\n".join(report)

class ASTParser:
    """Parser for Python AST analysis."""
    
    def __init__(self, source_code: str):
        self.source_code = source_code
        self.tree = None
        
    def parse(self) -> ast.AST:
        """Parse source code into AST."""
        try:
            self.tree = ast.parse(self.source_code)
            return self.tree
        except SyntaxError as e:
            raise ParseError(f"Failed to parse code: {str(e)}")
            
    def analyze(self) -> Dict[str, Any]:
        """Analyze AST and extract information."""
        if not self.tree:
            self.parse()
            
        return {
            'imports': self._find_imports(),
            'classes': self._find_classes(),
            'functions': self._find_functions(),
            'globals': self._find_globals()
        }
        
    def _find_imports(self) -> Set[str]:
        """Find all imports in the AST."""
        imports = set()
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Import):
                for name in node.names:
                    imports.add(name.name)
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ''
                for name in node.names:
                    if name.name == '*':
                        imports.add(f"{module}.*")
                    else:
                        imports.add(f"{module}.{name.name}")
        return imports
        
    def _find_classes(self) -> Set[str]:
        """Find all class definitions."""
        classes = set()
        for node in ast.walk(self.tree):
            if isinstance(node, ast.ClassDef):
                classes.add(node.name)
        return classes
        
    def _find_functions(self) -> Set[str]:
        """Find all function definitions."""
        functions = set()
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef):
                functions.add(node.name)
            elif isinstance(node, ast.AsyncFunctionDef):
                functions.add(node.name)
        return functions
        
    def _find_globals(self) -> Set[str]:
        """Find all global variables."""
        globals_vars = set()
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Global):
                globals_vars.update(node.names)
        return globals_vars 