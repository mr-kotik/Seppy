# API Documentation

## Core Classes

### Seppy

The main class for code analysis and documentation generation.

```python
class Seppy:
    def __init__(self, source_file: str, config_file: Optional[str] = None):
        """Initialize Seppy analyzer.
        
        Args:
            source_file: Path to the Python file to analyze
            config_file: Optional path to configuration file
        """
        pass
    
    def analyze_imports(self) -> Dict[str, Set[str]]:
        """Analyze imports in the source file.
        
        Returns:
            Dictionary mapping module names to their imports
        """
        pass
    
    def generate_docs(self, output_dir: str) -> None:
        """Generate documentation for the analyzed code.
        
        Args:
            output_dir: Directory to save generated documentation
        """
        pass
    
    def get_module_info(self) -> ModuleInfo:
        """Get detailed information about the analyzed module.
        
        Returns:
            ModuleInfo object containing module details
        """
        pass
```

### ModuleInfo

Class containing detailed information about a Python module.

```python
@dataclass
class ModuleInfo:
    """Information about a module."""
    name: str                # Module name
    code: str               # Source code
    imports: Set[str]       # Import statements
    global_vars: Set[str]   # Global variables
    functions: Set[str]     # Function definitions
    classes: Set[str]       # Class definitions
    async_functions: Set[str] = field(default_factory=set)  # Async functions
    dependencies: Set[str] = field(default_factory=set)     # Module dependencies
    docstring: Optional[str] = None                         # Module docstring
    decorators: Set[str] = field(default_factory=set)       # Module decorators
    docs: str = ""                                          # Generated documentation
```

### CacheData

Class for storing cached analysis data.

```python
@dataclass
class CacheData:
    """Class for storing cached data."""
    docs: str    # Generated documentation
    hash: str    # Content hash
```

### ProcessingStats

Class for tracking code analysis statistics.

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
        Dictionary containing analysis results
    """
    pass

def find_used_imports(node: ast.AST, all_imports: Set[str]) -> Set[str]:
    """Find imports that are actually used in the code.
    
    Args:
        node: AST node to analyze
        all_imports: Set of all import statements
        
    Returns:
        Set of used imports
    """
    pass

def find_used_globals(node: ast.AST, global_vars: Set[str]) -> Set[str]:
    """Find global variables that are used in the code.
    
    Args:
        node: AST node to analyze
        global_vars: Set of global variable names
        
    Returns:
        Set of used global variables
    """
    pass
```

## Processors

### Code Processing Functions

```python
def create_module_code(imports: Set[str], code: str) -> str:
    """Create module code with organized imports.
    
    Args:
        imports: Set of import statements
        code: Source code
        
    Returns:
        Formatted module code
    """
    pass

def create_module_docs(module_name: str, code: str) -> str:
    """Create documentation for a module.
    
    Args:
        module_name: Name of the module
        code: Source code
        
    Returns:
        Generated markdown documentation
    """
    pass

def organize_imports(imports: Set[str]) -> str:
    """Organize imports into a formatted string.
    
    Args:
        imports: Set of import statements
        
    Returns:
        Formatted import statements
    """
    pass
```

## Utilities

### Helper Functions

```python
@time_operation(operation_name: str)
def measure_time(func):
    """Decorator for measuring operation execution time.
    
    Args:
        operation_name: Name of the operation to measure
        
    Returns:
        Decorated function
    """
    pass

def setup_logging(level: str = "INFO") -> None:
    """Configure logging with rich formatting.
    
    Args:
        level: Logging level (default: INFO)
    """
    pass
```

## Configuration

### Configuration Options

```python
class Config:
    """Configuration settings for Seppy."""
    IGNORE_PATTERNS: List[str] = ["*.pyc", "__pycache__/*"]
    MEMORY_LIMIT_MB: int = 1024
    MAX_THREADS: int = 4
    CACHE_ENABLED: bool = True
    REPORT_FORMAT: str = "md"
    LOG_LEVEL: str = "INFO"
```

## Exception Classes

```python
class SeppyError(Exception):
    """Base exception for Seppy errors."""
    pass

class ParseError(SeppyError):
    """Raised when code parsing fails."""
    pass

class ConfigError(SeppyError):
    """Raised when configuration is invalid."""
    pass

class MemoryError(SeppyError):
    """Raised when memory limit is exceeded."""
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