# Seppy - Python Code Analysis Tool

Python 3.7+ | License: MIT

Seppy (Script sEparation in PYthon) is a powerful tool for analyzing Python code and generating comprehensive documentation. It uses AST-based parsing to understand code structure and relationships between different components.

## Key Features

* 🔍 Smart code analysis based on AST parsing
* 📊 Dependency tracking and visualization
* 📝 Comprehensive documentation generation
* ⚡ Full async/await support
* 🔍 Type hint preservation
* 🎨 Code style maintenance
* ⚙️ Highly configurable
* 📈 Performance monitoring
* 💾 Intelligent caching

## Supported Python Features

* ✅ All basic Python structures (functions, classes, variables)
* ✅ Async/await syntax and async context managers
* ✅ Type hints and annotations
* ✅ Decorators (with and without arguments)
* ✅ Context managers (with statements)
* ✅ Dataclasses and Protocols
* ✅ Generic types and type aliases
* ✅ Nested classes and functions
* ✅ Property methods and descriptors
* ✅ Match statements (Python 3.10+)
* ✅ Modern Python features (f-strings, walrus operator)
* ✅ Comprehensive docstring support

## Quick Installation

```bash
pip install seppy
```

Or install from source:

```bash
git clone https://github.com/mr-kotik/seppy.git
cd seppy
pip install -e .
```

## Quick Start

### Python API

```python
from seppy import Seppy

# Initialize analyzer
analyzer = Seppy("example.py")

# Generate documentation
analyzer.generate_docs("docs/")

# Get module information
module_info = analyzer.get_module_info()
print(f"Module name: {module_info.name}")
print(f"Functions: {module_info.functions}")
print(f"Classes: {module_info.classes}")
```

## Configuration

Seppy can be configured using YAML files:

```yaml
# config.yaml
IGNORE_PATTERNS:
  - "*.pyc"
  - "__pycache__/*"
MEMORY_LIMIT_MB: 1024
MAX_THREADS: 4
CACHE_ENABLED: true
REPORT_FORMAT: "md"
LOG_LEVEL: "INFO"
```

## Documentation

For detailed documentation, please see:

* [User Guide](docs/index.md)
* [API Reference](docs/api.md)
* [Configuration Guide](docs/configuration.md)
* [Examples](docs/examples.md)

## Example Output

For a given input file:

```python
class DataProcessor:
    async def process_data(self, data: list) -> dict:
        """Process input data asynchronously."""
        async with self.session as session:
            result = await self._transform(data)
            return result

    @property
    def is_ready(self) -> bool:
        """Check if processor is ready."""
        return self._ready
```

Seppy will generate comprehensive documentation including:

* Class and method signatures
* Type hints
* Docstrings
* Async/await syntax
* Property decorators
* Context managers

## Requirements

* Python 3.7+
* Dependencies listed in requirements.txt

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 
