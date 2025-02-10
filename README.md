# Seppy - Python Script Splitter

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Seppy (Script sEparation in PYthon) is a powerful tool for splitting large Python scripts into smaller, more manageable modules. It analyzes Python code and intelligently separates it into logical components while maintaining dependencies and relationships between different parts of the code.

## Key Features

- 🔄 Smart code splitting based on classes and functions
- 📊 Dependency tracking and visualization
- 📝 Automatic documentation generation
- ⚡ Async code support
- ⚙️ Highly configurable
- 📈 Performance monitoring
- 💾 Caching for faster processing

## Quick Installation

```bash
# Install from source
git clone https://github.com/yourusername/seppy.git
cd seppy
pip install -e .

# Or install dependencies only
pip install -r requirements.txt
```

## Quick Start

```bash
# Basic usage
seppy your_script.py

# With all options
seppy your_script.py -o output_dir -c config.yaml -m 2048 -v
```

Or use as a Python package:

```python
from seppy import Seppy

# Initialize and process
splitter = Seppy("your_script.py")
modules = splitter.parse_script("your_script.py")
splitter.save_modules("output_directory")
```

## Documentation

For detailed documentation, please see:
- [User Guide](docs/index.md)
- [API Reference](docs/api.md)
- [Configuration](docs/configuration.md)
- [Examples](docs/examples.md)

## Requirements

- Python 3.7+
- Dependencies listed in requirements.txt

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 
