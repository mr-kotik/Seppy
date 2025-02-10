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
def analyze_complex_structures(node: ast.AST, source_code: str = '') -> Dict[str, Any]:
    """Analyze complex code structures.
    
    Supported structures:
    - Functions and methods (sync/async)
    - Classes and inheritance
    - Decorators and annotations
    - Type hints and aliases
    - Context managers
    - Control flow structures
    - Comprehensions and generators
    - Modern Python features
    
    Args:
        node: AST node to analyze
        source_code: Original source code for preserving formatting
        
    Returns:
        Dictionary containing analyzed structures
    """
    pass

def find_used_imports(node: ast.AST, all_imports: Set[str]) -> Set[str]:
    """Find imports that are actually used in the code."""
    pass

def find_used_globals(node: ast.AST, global_vars: Set[str]) -> Set[str]:
    """Find global variables that are used in the code."""
    pass

def extract_imports(tree: ast.AST, *nodes) -> Set[str]:
    """Extract all imports from AST nodes."""
    pass
```

## Processors

### Code Processing Functions

```python
def create_complex_module(name: str, node: ast.AST, structures: Dict[str, Any]) -> str:
    """Create a module from complex code structures.
    
    Handles:
    - Type aliases and generic types
    - Constants and variables
    - Import statements
    - Function and method definitions
    - Class definitions with inheritance
    - Nested classes and functions
    - Decorators and annotations
    - Context managers and control flow
    - Modern Python features
    
    Args:
        name: Name of the module
        node: AST node to process
        structures: Dictionary of analyzed structures
        
    Returns:
        Generated module code as string
    """
    pass

def create_module_docs(module_name: str, code: str) -> str:
    """Create documentation for a module.
    
    Generates:
    - Module overview
    - Import statements
    - Function and method documentation
    - Class documentation
    - Type information
    - Usage examples
    
    Args:
        module_name: Name of the module
        code: Source code of the module
        
    Returns:
        Generated markdown documentation
    """
    pass

def organize_imports(imports: Set[str]) -> str:
    """Organize imports into a formatted string.
    
    Organizes imports into sections:
    - Standard library imports
    - Third-party imports
    - Local imports
    
    Args:
        imports: Set of import statements
        
    Returns:
        Formatted import section
    """
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

### Advanced Usage

```python
from seppy import Seppy

# Initialize with configuration
splitter = Seppy(
    source_file="complex_script.py",
    config_file="config.yaml",
    memory_limit_mb=2048
)

# Process and analyze
modules = splitter.parse_script("complex_script.py")

# Save with documentation
splitter.save_modules("output_modules")
```

### Error Handling

```python
from seppy import Seppy, ParseError, ModuleProcessingError

try:
    splitter = Seppy("script.py")
    modules = splitter.parse_script("script.py")
    splitter.save_modules("output")
except ParseError as e:
    print(f"Parse error: {e}")
except ModuleProcessingError as e:
    print(f"Processing error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}") 