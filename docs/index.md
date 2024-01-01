# Seppy Documentation

Seppy is a powerful Python code analysis and documentation generation tool that helps developers understand and maintain their Python projects.

## Features

- **Code Analysis**:
  - AST-based parsing
  - Dependency tracking
  - Import analysis
  - Code structure analysis
  - Type hint validation

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

#### From PyPI
```bash
pip install seppy
```

#### From Source
```bash
git clone https://github.com/mr-kotik/seppy.git
cd seppy
pip install -e .
```

## Quick Start

```python
from seppy import Seppy

# Initialize Seppy with your Python file
analyzer = Seppy("your_script.py")

# Generate documentation
analyzer.generate_docs("docs/")

# Analyze imports
imports = analyzer.analyze_imports()

# Get module information
module_info = analyzer.get_module_info()
```

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 