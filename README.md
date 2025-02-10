# Seppy - Python Script Splitter

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Seppy (Script sEparation in PYthon) is a powerful tool for splitting large Python scripts into smaller, more manageable modules. It analyzes Python code and intelligently separates it into logical components while maintaining dependencies and relationships between different parts of the code.

## Key Features

- 🔄 Smart code splitting based on code structure analysis
- 📊 Dependency tracking and visualization
- 📝 Comprehensive documentation generation
- ⚡ Full async/await support
- 🔍 Type hint preservation
- 🎨 Code style maintenance
- ⚙️ Highly configurable
- 📈 Performance monitoring
- 💾 Intelligent caching

## Supported Python Features

- ✅ All basic Python structures (functions, classes, variables)
- ✅ Async/await syntax and async context managers
- ✅ Type hints and annotations
- ✅ Decorators (with and without arguments)
- ✅ Context managers (with statements)
- ✅ Dataclasses and Protocols
- ✅ Generic types and type aliases
- ✅ Nested classes and functions
- ✅ Property methods and descriptors
- ✅ Match statements (Python 3.10+)
- ✅ Modern Python features (f-strings, walrus operator)
- ✅ Comprehensive docstring support

## Quick Installation

```bash
pip install seppy
```

Or install from source:

```bash
git clone https://github.com/yourusername/seppy.git
cd seppy
pip install -e .
```

## Quick Start

### Command Line

```bash
# Basic usage
seppy your_script.py

# With output directory
seppy your_script.py -o output_dir

# With configuration
seppy your_script.py -c config.yaml -m 2048 -v
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

# Process script
modules = splitter.parse_script("your_script.py")

# Save modules
splitter.save_modules("output_dir")
```

## Configuration

Seppy can be configured using YAML or JSON files:

```yaml
# config.yaml
IGNORE_PATTERNS:
  - "*.pyc"
  - "__pycache__/*"
MEMORY_LIMIT_MB: 2048
MAX_THREADS: 4
FEATURES:
  async_support: true
  type_hints: true
  docstrings: true
CODE_STYLE:
  indent_size: 4
  line_length: 88
  sort_imports: true
```

## Documentation

For detailed documentation, please see:
- [User Guide](docs/index.md)
- [API Reference](docs/api.md)
- [Configuration Guide](docs/configuration.md)
- [Examples](docs/examples.md)

## Example Output

For a given input script:

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

Seppy will generate:

```
output_dir/
├── data_processor/
│   ├── __init__.py
│   ├── processor.py
│   └── utils.py
├── docs/
│   ├── data_processor.md
│   └── api.md
└── dependencies.json
```

With proper preservation of:
- Async/await syntax
- Type hints
- Docstrings
- Property decorators
- Context managers

## Requirements

- Python 3.7+
- Dependencies listed in requirements.txt

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 