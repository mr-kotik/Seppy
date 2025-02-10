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
MEMORY_LIMIT_MB: 1024
MAX_THREADS: 4
CACHE_ENABLED: true
REPORT_FORMAT: "md"
LOG_LEVEL: "INFO"
```

### JSON Format

```json
{
  "IGNORE_PATTERNS": [
    "*.pyc",
    "__pycache__/*",
    ".*"
  ],
  "MEMORY_LIMIT_MB": 1024,
  "MAX_THREADS": 4,
  "CACHE_ENABLED": true,
  "REPORT_FORMAT": "md",
  "LOG_LEVEL": "INFO"
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
MEMORY_LIMIT_MB: 1024  # 1GB limit
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

### REPORT_FORMAT

Format for generated documentation.

```yaml
REPORT_FORMAT: "md"  # Markdown format
```

Available formats:
- `"md"` - Markdown (default)
- `"rst"` - reStructuredText
- `"txt"` - Plain text

### LOG_LEVEL

Logging verbosity level.

```yaml
LOG_LEVEL: "INFO"
```

Available levels:
- `"DEBUG"` - Detailed debugging information
- `"INFO"` - General information (default)
- `"WARNING"` - Warning messages only
- `"ERROR"` - Error messages only
- `"CRITICAL"` - Critical errors only

## Advanced Configuration

### Cache Configuration

```yaml
CACHE_VERSION: "1.0.0"
MAX_CACHE_SIZE: 1073741824  # 1GB in bytes
CACHE_CLEANUP_THRESHOLD: 0.9  # 90%
```

### Memory Management

```yaml
MEMORY_CHECK_INTERVAL: 60  # seconds
MIN_MEMORY_LIMIT: 256     # MB
MAX_MEMORY_LIMIT: 8192    # MB
```

### File Operations

```yaml
MAX_LINES_PER_READ: 250
DEFAULT_ENCODING: "utf-8"
```

## Command Line Arguments

Command line arguments override configuration file settings:

```bash
seppy script.py -m 2048 -v
```

Priority order:
1. Command line arguments
2. Configuration file
3. Default values

## Environment Variables

Seppy also respects the following environment variables:

```bash
SEPPY_CONFIG_FILE=/path/to/config.yaml
SEPPY_MEMORY_LIMIT=2048
SEPPY_LOG_LEVEL=DEBUG
```

## Configuration Best Practices

1. **Start with Defaults**
   ```yaml
   MEMORY_LIMIT_MB: 1024
   MAX_THREADS: 4
   CACHE_ENABLED: true
   ```

2. **Adjust for Large Projects**
   ```yaml
   MEMORY_LIMIT_MB: 4096
   MAX_THREADS: 8
   CACHE_ENABLED: true
   ```

3. **Debug Configuration**
   ```yaml
   LOG_LEVEL: "DEBUG"
   CACHE_ENABLED: false
   MEMORY_CHECK_INTERVAL: 30
   ```

## Example Configurations

### Minimal Configuration
```yaml
IGNORE_PATTERNS:
  - "*.pyc"
MEMORY_LIMIT_MB: 1024
MAX_THREADS: 4
```

### Development Configuration
```yaml
IGNORE_PATTERNS:
  - "*.pyc"
  - "__pycache__/*"
  - "venv/*"
  - ".git/*"
MEMORY_LIMIT_MB: 2048
MAX_THREADS: 4
CACHE_ENABLED: true
LOG_LEVEL: "DEBUG"
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
REPORT_FORMAT: "md"
``` 