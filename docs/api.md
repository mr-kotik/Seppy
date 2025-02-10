# Seppy API Reference

This document provides detailed information about Seppy's API components.

## Table of Contents

1. [Core API](#core-api)
2. [Models](#models)
3. [Analyzers](#analyzers)
4. [Processors](#processors)
5. [Utilities](#utilities)
6. [Exceptions](#exceptions)

## Core API

### Seppy Class

The main class for script splitting operations.

```python
class Seppy:
    def __init__(
        self,
        source_file: str,
        config_file: Optional[str] = None,
        memory_limit_mb: Optional[int] = None
    ):
        """Initialize Seppy instance.
        
        Args:
            source_file: Path to the source Python file
            config_file: Optional path to configuration file
            memory_limit_mb: Optional memory limit override
        """
        pass

    def parse_script(self, source_file: str) -> Dict[str, ModuleInfo]:
        """Parse Python script and extract module information.
        
        Args:
            source_file: Path to the Python file to parse
            
        Returns:
            Dictionary mapping module names to ModuleInfo objects
            
        Raises:
            ParseError: If script parsing fails
            ModuleProcessingError: If module processing fails
        """
        pass

    def save_modules(self, output_dir: str):
        """Save split modules to files.
        
        Args:
            output_dir: Directory to save modules in
            
        Raises:
            IOError: If file operations fail
        """
        pass
```

## Models

### ModuleInfo

```python
@dataclass
class ModuleInfo:
    """Information about a module."""
    name: str              # Module name
    code: str             # Module source code
    imports: Set[str]     # Import statements
    global_vars: Set[str] # Global variables
    functions: Set[str]   # Function definitions
    classes: Set[str]     # Class definitions
    async_functions: Set[str] = field(default_factory=set)
    dependencies: Set[str] = field(default_factory=set)
    docstring: Optional[str] = None
    decorators: Set[str] = field(default_factory=set)
    docs: str = ""
```

### CacheData

```python
@dataclass
class CacheData:
    """Class for storing cached data."""
    docs: str    # Generated documentation
    hash: str    # Content hash
```

### ProcessingStats

```python
@dataclass
class ProcessingStats:
    """Statistics about script processing."""
    total_modules: int = 0
    processed_modules: int = 0
    failed_modules: int = 0
    cached_modules: int = 0
    processing_time: float = 0.0
    memory_usage: List[int] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
```

## Analyzers

### Code Analysis Functions

```python
def find_used_imports(node: ast.AST, all_imports: Set[str]) -> Set[str]:
    """Find imports that are actually used in the code."""
    pass

def find_used_globals(node: ast.AST, global_vars: Set[str]) -> Set[str]:
    """Find global variables that are used in the code."""
    pass

def extract_imports(tree: ast.AST, *nodes) -> Set[str]:
    """Extract all imports from AST nodes."""
    pass

def analyze_complex_structures(node: ast.AST) -> Dict[str, Any]:
    """Analyze complex code structures like nested classes and functions."""
    pass
```

## Processors

### Code Processing Functions

```python
def organize_imports(imports: Set[str]) -> str:
    """Organize imports into a formatted string."""
    pass

def create_module_code(imports: Set[str], code: str) -> str:
    """Create module code with organized imports."""
    pass

def create_module_docs(module_name: str, code: str) -> str:
    """Create documentation for a module."""
    pass

def create_complex_module(name: str, node: ast.AST, structures: Dict[str, Any]) -> str:
    """Create a module from complex code structures."""
    pass
```

## Utilities

### Decorators

```python
def time_operation(operation_name: str):
    """Decorator for measuring operation execution time."""
    pass
```

### Configuration

```python
class SeppyConfig(TypedDict):
    """Configuration type definition."""
    IGNORE_PATTERNS: List[str]
    MEMORY_LIMIT_MB: int
    MAX_THREADS: int
    CACHE_ENABLED: bool
    REPORT_FORMAT: str
    LOG_LEVEL: str
```

## Exceptions

```python
class ScriptSplitterError(Exception):
    """Base class for ScriptSplitter errors."""
    pass

class ParseError(ScriptSplitterError):
    """Error during code parsing."""
    pass

class ModuleProcessingError(ScriptSplitterError):
    """Error during module processing."""
    pass

class CacheError(ScriptSplitterError):
    """Error during cache operations."""
    pass
```

## Usage Examples

### Basic Usage

```python
from seppy import Seppy

# Initialize
splitter = Seppy("script.py")

# Process
modules = splitter.parse_script("script.py")

# Save
splitter.save_modules("output")
```

### With Configuration

```python
from seppy import Seppy, SeppyConfig

config: SeppyConfig = {
    "IGNORE_PATTERNS": ["*.pyc"],
    "MEMORY_LIMIT_MB": 2048,
    "MAX_THREADS": 4,
    "CACHE_ENABLED": True,
    "REPORT_FORMAT": "md",
    "LOG_LEVEL": "INFO"
}

splitter = Seppy(
    "script.py",
    config_file="config.yaml",
    memory_limit_mb=2048
)
```

### Error Handling

```python
from seppy import Seppy, ParseError, ModuleProcessingError

try:
    splitter = Seppy("script.py")
    modules = splitter.parse_script("script.py")
except ParseError as e:
    print(f"Parse error: {e}")
except ModuleProcessingError as e:
    print(f"Processing error: {e}")
``` 