# Seppy Documentation

Welcome to the comprehensive documentation for Seppy, a powerful Python script splitting tool.

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Basic Usage](#basic-usage)
4. [Advanced Usage](#advanced-usage)
5. [Supported Structures](#supported-structures)
6. [Configuration](#configuration)
7. [Output Structure](#output-structure)
8. [Best Practices](#best-practices)
9. [Troubleshooting](#troubleshooting)

## Introduction

Seppy is designed to help developers manage large Python codebases by intelligently splitting monolithic scripts into smaller, more maintainable modules. It analyzes code structure, dependencies, and relationships to create a logical separation of concerns.

### Key Features in Detail

- **Smart Code Splitting**: Analyzes code structure and splits based on:
  - Class definitions
  - Function definitions
  - Module-level variables
  - Import statements
  - Dependencies between components

- **Dependency Analysis**: 
  - Tracks function calls
  - Maps class inheritance
  - Identifies shared variables
  - Creates dependency graphs

- **Documentation Generation**:
  - Preserves docstrings
  - Generates markdown documentation
  - Creates module summaries
  - Maintains cross-references

## Supported Structures

Seppy supports all major Python language structures:

### Basic Structures
- Variables and assignments
- Functions and methods
- Classes and inheritance
- Import statements
- Docstrings
- Type hints and annotations

### Advanced Structures
1. **Control Flow**:
   - If/elif/else statements
   - For/while loops with else clauses
   - Match/case statements (Python 3.10+)
   - Try/except/else/finally blocks

2. **Context Managers**:
   - With statements
   - Async with statements
   - Multiple context managers
   - Context manager aliases

3. **Functions and Methods**:
   - Regular functions
   - Async functions
   - Generator functions
   - Lambda functions
   - Nested functions
   - Method types:
     - Instance methods
     - Class methods
     - Static methods
     - Abstract methods
     - Property methods

4. **Classes and Types**:
   - Regular classes
   - Dataclasses
   - Abstract base classes
   - Protocols
   - Generic types
   - Type aliases
   - Type variables
   - ClassVar annotations

5. **Comprehensions and Generators**:
   - List comprehensions
   - Set comprehensions
   - Dict comprehensions
   - Generator expressions

6. **Decorators**:
   - Function decorators
   - Class decorators
   - Method decorators
   - Decorators with arguments

7. **Asynchronous Programming**:
   - Async functions
   - Async with statements
   - Async for loops
   - Await expressions
   - Async context managers

8. **Modern Python Features**:
   - f-strings
   - Walrus operator (:=)
   - Type comments
   - Match statements
   - Positional-only parameters
   - Keyword-only parameters
   - Variable annotations

9. **Special Methods**:
   - Magic methods
   - Property methods
   - Descriptors
   - Context manager methods

10. **Module-Level Features**:
    - Module docstrings
    - Import statements
    - Import aliases
    - Wildcard imports
    - Future imports
    - Type hints

## Installation

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Installation Methods

1. **From Source (Recommended for Development)**:
   ```bash
   git clone https://github.com/yourusername/seppy.git
   cd seppy
   pip install -e .
   ```

2. **Using Requirements File**:
   ```bash
   pip install -r requirements.txt
   ```

### Verifying Installation

```bash
seppy --version
```

## Basic Usage

### Command Line Interface

1. **Basic Command**:
   ```bash
   seppy your_script.py
   ```

2. **With Output Directory**:
   ```bash
   seppy your_script.py -o ./modules
   ```

3. **With Configuration**:
   ```bash
   seppy your_script.py -c config.yaml
   ```

### Python API

```python
from seppy import Seppy

# Initialize
splitter = Seppy(
    source_file="your_script.py",
    config_file="config.yaml",
    memory_limit_mb=2048
)

# Process
modules = splitter.parse_script("your_script.py")

# Save results
splitter.save_modules("output_directory")
```

## Advanced Usage

### Command Line Options

```bash
seppy your_script.py [OPTIONS]

Options:
  -o, --output DIR         Output directory (default: output)
  -c, --config FILE        Configuration file path
  -m, --memory-limit MB    Memory limit in megabytes
  -v, --verbose           Enable verbose logging
  --help                  Show this help message
```

### Configuration File

The configuration file can be in JSON or YAML format:

```yaml
# config.yaml
IGNORE_PATTERNS:
  - "*.pyc"
  - "__pycache__/*"
  - ".*"
MEMORY_LIMIT_MB: 1024
MAX_THREADS: 4
CACHE_ENABLED: true
REPORT_FORMAT: "md"
LOG_LEVEL: "INFO"
```

### Advanced Features

1. **Caching**:
   - Enable caching for faster processing
   - Configure cache size and cleanup
   - Use cache versioning

2. **Memory Management**:
   - Set memory limits
   - Monitor usage
   - Automatic cleanup

3. **Parallel Processing**:
   - Configure thread count
   - Process large files efficiently
   - Handle async code

## Output Structure

```
output_directory/
├── modules/
│   ├── module1.py
│   ├── module2.py
│   └── ...
├── docs/
│   ├── module1.md
│   ├── module2.md
│   └── ...
├── dependencies.json
└── report.md
```

### Module Structure

Each generated module follows this structure:
```python
"""Module docstring preserved from original."""

# Imports section
from typing import Optional
import required_module

# Classes section
class ExampleClass:
    """Class docstring preserved."""
    ...

# Functions section
def example_function():
    """Function docstring preserved."""
    ...
```

## Best Practices

1. **Input Code Organization**:
   - Use consistent naming
   - Add proper docstrings
   - Follow PEP 8 guidelines

2. **Configuration**:
   - Start with default settings
   - Adjust based on project size
   - Monitor performance

3. **Output Management**:
   - Use version control
   - Review generated modules
   - Validate dependencies

## Troubleshooting

### Common Issues

1. **Memory Errors**:
   - Increase memory limit
   - Reduce input file size
   - Enable caching

2. **Parse Errors**:
   - Check syntax errors
   - Validate input file
   - Check Python version

3. **Performance Issues**:
   - Adjust thread count
   - Enable caching
   - Monitor system resources

### Error Messages

| Error | Description | Solution |
|-------|-------------|----------|
| `ParseError` | Failed to parse input file | Check file syntax |
| `MemoryError` | Exceeded memory limit | Increase limit or split input |
| `ConfigError` | Invalid configuration | Check config file format |

## Support

For additional support:
- Create an issue on GitHub
- Check the FAQ section
- Join our community discussions 