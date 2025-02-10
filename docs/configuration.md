# Seppy Configuration Guide

This document describes all available configuration options for Seppy.

## Configuration Methods

Seppy can be configured in several ways:

1. Using a configuration file (YAML or JSON)
2. Through command-line arguments
3. Programmatically via the Python API

## Configuration File Format

### YAML Format (Recommended)

```yaml
# config.yaml
IGNORE_PATTERNS:
  - "*.pyc"
  - "__pycache__/*"
  - ".*"
  - "test_*.py"
  - "venv/*"
MEMORY_LIMIT_MB: 2048
MAX_THREADS: 4
CACHE_ENABLED: true
REPORT_FORMAT: "md"
LOG_LEVEL: "INFO"
CODE_STYLE:
  indent_size: 4
  line_length: 88
  sort_imports: true
FEATURES:
  async_support: true
  type_hints: true
  docstrings: true
  nested_classes: true
  decorators: true
DOCUMENTATION:
  generate_examples: true
  include_source: true
  format: "markdown"
  sections:
    - "overview"
    - "classes"
    - "functions"
    - "types"
```

### JSON Format

```json
{
  "IGNORE_PATTERNS": [
    "*.pyc",
    "__pycache__/*",
    ".*",
    "test_*.py",
    "venv/*"
  ],
  "MEMORY_LIMIT_MB": 2048,
  "MAX_THREADS": 4,
  "CACHE_ENABLED": true,
  "REPORT_FORMAT": "md",
  "LOG_LEVEL": "INFO",
  "CODE_STYLE": {
    "indent_size": 4,
    "line_length": 88,
    "sort_imports": true
  },
  "FEATURES": {
    "async_support": true,
    "type_hints": true,
    "docstrings": true,
    "nested_classes": true,
    "decorators": true
  },
  "DOCUMENTATION": {
    "generate_examples": true,
    "include_source": true,
    "format": "markdown",
    "sections": [
      "overview",
      "classes",
      "functions",
      "types"
    ]
  }
}
```

## Configuration Options

### IGNORE_PATTERNS

List of glob patterns for files to ignore during processing.

```yaml
IGNORE_PATTERNS:
  - "*.pyc"        # Ignore compiled Python files
  - "__pycache__/*" # Ignore cache directories
  - ".*"           # Ignore hidden files
  - "test_*.py"    # Ignore test files
  - "venv/*"       # Ignore virtual environment
```

### MEMORY_LIMIT_MB

Memory limit in megabytes for the processing.

```yaml
MEMORY_LIMIT_MB: 2048  # 2GB limit
```

- Minimum: 256 MB
- Maximum: 8192 MB (8GB)
- Default: 1024 MB (1GB)

### MAX_THREADS

Number of threads to use for parallel processing.

```yaml
MAX_THREADS: 4
```

- Minimum: 1
- Maximum: 16
- Default: 4

### CACHE_ENABLED

Enable or disable caching of processed files.

```yaml
CACHE_ENABLED: true
```

When enabled:
- Speeds up repeated processing
- Stores results in `.seppy_cache` directory
- Automatically manages cache size

### CODE_STYLE

Code style preferences for generated modules.

```yaml
CODE_STYLE:
  indent_size: 4        # Number of spaces for indentation
  line_length: 88       # Maximum line length
  sort_imports: true    # Sort imports by type
  wrap_long_lines: true # Wrap lines exceeding max length
  spaces_around_ops: true # Add spaces around operators
```

### FEATURES

Control which Python features to support.

```yaml
FEATURES:
  async_support: true    # Support async/await syntax
  type_hints: true      # Include type hints
  docstrings: true      # Preserve docstrings
  nested_classes: true  # Support nested class definitions
  decorators: true      # Support decorators
  dataclasses: true     # Support dataclass features
  protocols: true       # Support Protocol classes
  generics: true        # Support generic types
```

### DOCUMENTATION

Documentation generation settings.

```yaml
DOCUMENTATION:
  generate_examples: true   # Generate usage examples
  include_source: true     # Include source code
  format: "markdown"       # Documentation format
  sections:               # Sections to include
    - "overview"
    - "classes"
    - "functions"
    - "types"
  code_blocks: true       # Include code blocks
  cross_references: true  # Add cross-references
```

## Advanced Configuration

### Cache Configuration

```yaml
CACHE_VERSION: "1.0.0"
MAX_CACHE_SIZE: 1073741824  # 1GB in bytes
CACHE_CLEANUP_THRESHOLD: 0.9  # 90%
CACHE_TTL: 86400           # 24 hours in seconds
```

### Memory Management

```yaml
MEMORY_CHECK_INTERVAL: 60  # seconds
MIN_MEMORY_LIMIT: 256     # MB
MAX_MEMORY_LIMIT: 8192    # MB
GC_THRESHOLD: 0.8         # Trigger GC at 80% memory usage
```

### Processing Options

```yaml
PROCESSING:
  parallel_enabled: true
  max_file_size: 10485760  # 10MB
  timeout: 300             # 5 minutes
  retries: 3
  batch_size: 100
```

## Environment Variables

Seppy respects the following environment variables:

```bash
SEPPY_CONFIG_FILE=/path/to/config.yaml
SEPPY_MEMORY_LIMIT=2048
SEPPY_LOG_LEVEL=DEBUG
SEPPY_CACHE_DIR=/path/to/cache
SEPPY_MAX_THREADS=8
```

## Configuration Best Practices

1. **Development Configuration**
   ```yaml
   MEMORY_LIMIT_MB: 1024
   MAX_THREADS: 4
   CACHE_ENABLED: true
   LOG_LEVEL: "DEBUG"
   FEATURES:
     async_support: true
     type_hints: true
   ```

2. **Production Configuration**
   ```yaml
   MEMORY_LIMIT_MB: 4096
   MAX_THREADS: 8
   CACHE_ENABLED: true
   LOG_LEVEL: "WARNING"
   FEATURES:
     async_support: true
     type_hints: true
   ```

3. **Documentation Generation**
   ```yaml
   DOCUMENTATION:
     generate_examples: true
     include_source: true
     format: "markdown"
     sections:
       - "overview"
       - "classes"
       - "functions"
     code_blocks: true
   ```

## Example Configurations

### Minimal Configuration
```yaml
IGNORE_PATTERNS:
  - "*.pyc"
MEMORY_LIMIT_MB: 1024
MAX_THREADS: 4
CACHE_ENABLED: true
```

### Full Development Configuration
```yaml
IGNORE_PATTERNS:
  - "*.pyc"
  - "__pycache__/*"
  - "venv/*"
  - ".git/*"
  - "tests/*"
MEMORY_LIMIT_MB: 2048
MAX_THREADS: 4
CACHE_ENABLED: true
LOG_LEVEL: "DEBUG"
CODE_STYLE:
  indent_size: 4
  line_length: 88
  sort_imports: true
FEATURES:
  async_support: true
  type_hints: true
  docstrings: true
DOCUMENTATION:
  generate_examples: true
  include_source: true
  format: "markdown"
  sections:
    - "overview"
    - "classes"
    - "functions"
```

### Production Configuration
```yaml
IGNORE_PATTERNS:
  - "*.pyc"
  - "__pycache__/*"
  - ".*"
MEMORY_LIMIT_MB: 4096
MAX_THREADS: 8
CACHE_ENABLED: true
LOG_LEVEL: "WARNING"
CODE_STYLE:
  indent_size: 4
  line_length: 88
  sort_imports: true
FEATURES:
  async_support: true
  type_hints: true
  docstrings: true
DOCUMENTATION:
  generate_examples: false
  include_source: false
  format: "markdown"
  sections:
    - "overview"
    - "classes"
    - "functions"
``` 