import ast
from typing import Dict, Set, Any, Optional, List, Tuple
from .models import ModuleInfo

def find_used_imports(node: ast.AST, all_imports: Set[str]) -> Set[str]:
    """Find imports that are actually used in the code."""
    used_imports = set()
    for node in ast.walk(node):
        if isinstance(node, ast.Name) and node.id in all_imports:
            used_imports.add(node.id)
    return used_imports

def find_used_globals(node: ast.AST, global_vars: Set[str]) -> Set[str]:
    """Find global variables that are used in the code."""
    used_globals = set()
    for node in ast.walk(node):
        if isinstance(node, ast.Name) and node.id in global_vars:
            used_globals.add(node.id)
    return used_globals

def extract_imports(tree: ast.AST, *nodes) -> Set[str]:
    """Extract all imports from AST nodes."""
    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for name in node.names:
                imports.add(name.name)
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            for name in node.names:
                if name.name == "*":
                    imports.add(f"{module}.*")
                else:
                    imports.add(f"{module}.{name.name}")
    return imports

def get_parent_function_or_class(node: ast.AST, tree: ast.AST) -> Optional[str]:
    """Get the name of the parent function or class for a given node."""
    for parent in ast.walk(tree):
        if isinstance(parent, (ast.FunctionDef, ast.ClassDef)):
            for child in ast.walk(parent):
                if child == node:
                    return parent.name
    return None

def analyze_complex_structures(node: ast.AST) -> Dict[str, Any]:
    """Analyze complex code structures like nested classes and functions."""
    structures = {
        'classes': {},
        'functions': {},
        'imports': set(),
        'globals': set()
    }
    
    for child in ast.walk(node):
        if isinstance(child, ast.ClassDef):
            structures['classes'][child.name] = {
                'methods': [],
                'properties': [],
                'nested_classes': []
            }
            for item in child.body:
                if isinstance(item, ast.FunctionDef):
                    structures['classes'][child.name]['methods'].append(item.name)
                elif isinstance(item, ast.ClassDef):
                    structures['classes'][child.name]['nested_classes'].append(item.name)
        elif isinstance(child, ast.FunctionDef):
            structures['functions'][child.name] = {
                'args': [arg.arg for arg in child.args.args],
                'returns': None
            }
            if child.returns:
                structures['functions'][child.name]['returns'] = ast.unparse(child.returns)
                
    return structures

def get_parent_class(node: ast.ClassDef, tree: ast.AST) -> Optional[ast.ClassDef]:
    """Get the parent class node for a given class node."""
    for parent in ast.walk(tree):
        if isinstance(parent, ast.ClassDef):
            for child in ast.walk(parent):
                if child == node and child is not parent:
                    return parent
    return None

def is_node_in_function_or_class(node: ast.AST, tree: ast.AST) -> bool:
    """Check if a node is inside a function or class definition."""
    return get_parent_function_or_class(node, tree) is not None 