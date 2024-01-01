# Configuration Guide

This document describes the configuration options available in Seppy.

## Configuration File

Seppy can be configured using a YAML configuration file. The configuration file can be specified when initializing Seppy:

```python
from seppy import Seppy

analyzer = Seppy("example.py", config_file="config.yaml")
```

## Configuration Options

### Basic Configuration

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

### Option Details

#### IGNORE_PATTERNS
List of glob patterns for files to ignore during analysis.
- Default: `["*.pyc", "__pycache__/*"]`
- Example:
  ```yaml
  IGNORE_PATTERNS:
    - "*.pyc"
    - "__pycache__/*"
    - "test_*.py"
    - ".git/*"
  ```

#### MEMORY_LIMIT_MB
Maximum memory usage limit in megabytes.
- Default: `1024`
- Example:
  ```yaml
  MEMORY_LIMIT_MB: 2048
  ```

#### MAX_THREADS
Maximum number of threads to use for parallel processing.
- Default: `4`
- Example:
  ```yaml
  MAX_THREADS: 8
  ```

#### CACHE_ENABLED
Whether to enable caching of analysis results.
- Default: `true`
- Example:
  ```yaml
  CACHE_ENABLED: false
  ```

#### REPORT_FORMAT
Format for generated documentation.
- Default: `"md"`
- Supported values: `"md"`, `"rst"`
- Example:
  ```yaml
  REPORT_FORMAT: "rst"
  ```

#### LOG_LEVEL
Logging level for the application.
- Default: `"INFO"`
- Supported values: `"DEBUG"`, `"INFO"`, `"WARNING"`, `"ERROR"`, `"CRITICAL"`
- Example:
  ```yaml
  LOG_LEVEL: "DEBUG"
  ```

## Advanced Configuration

### Cache Configuration

```yaml
CACHE_CONFIG:
  DIRECTORY: ".cache"
  MAX_SIZE_MB: 512
  EXPIRATION_DAYS: 7
```

### Documentation Configuration

```yaml
DOCS_CONFIG:
  TEMPLATE_DIR: "templates"
  OUTPUT_FORMAT: "md"
  INCLUDE_PRIVATE: false
  INCLUDE_SOURCE: true
```

### Analysis Configuration

```yaml
ANALYSIS_CONFIG:
  MAX_FILE_SIZE_MB: 10
  IGNORE_DECORATORS:
    - "deprecated"
    - "experimental"
  PARSE_DOCSTRINGS: true
  TYPE_CHECK: true
```

## Environment Variables

Seppy also supports configuration through environment variables:

- `SEPPY_MEMORY_LIMIT`: Memory limit in MB
- `SEPPY_MAX_THREADS`: Maximum thread count
- `SEPPY_CACHE_ENABLED`: Enable/disable caching
- `SEPPY_LOG_LEVEL`: Logging level

Example:
```bash
export SEPPY_MEMORY_LIMIT=2048
export SEPPY_LOG_LEVEL=DEBUG
```

## Configuration Precedence

Configuration values are loaded in the following order (later sources override earlier ones):

1. Default values
2. Configuration file
3. Environment variables
4. Command-line arguments

## Example Configurations

### Development Configuration

```yaml
# dev_config.yaml
MEMORY_LIMIT_MB: 2048
MAX_THREADS: 8
CACHE_ENABLED: true
LOG_LEVEL: "DEBUG"
IGNORE_PATTERNS:
  - "*.pyc"
  - "__pycache__/*"
  - "test_*.py"
DOCS_CONFIG:
  INCLUDE_PRIVATE: true
  INCLUDE_SOURCE: true
```

### Production Configuration

```yaml
# prod_config.yaml
MEMORY_LIMIT_MB: 4096
MAX_THREADS: 16
CACHE_ENABLED: true
LOG_LEVEL: "WARNING"
IGNORE_PATTERNS:
  - "*.pyc"
  - "__pycache__/*"
  - "test_*.py"
  - "*.log"
DOCS_CONFIG:
  INCLUDE_PRIVATE: false
  INCLUDE_SOURCE: false
```

### Testing Configuration

```yaml
# test_config.yaml
MEMORY_LIMIT_MB: 1024
MAX_THREADS: 2
CACHE_ENABLED: false
LOG_LEVEL: "DEBUG"
IGNORE_PATTERNS:
  - "*.pyc"
  - "__pycache__/*"
DOCS_CONFIG:
  INCLUDE_PRIVATE: true
  INCLUDE_SOURCE: true
```

## Best Practices

1. **Memory Management**
   - Set `MEMORY_LIMIT_MB` based on available system resources
   - Monitor memory usage during analysis
   - Enable caching for large codebases

2. **Threading**
   - Set `MAX_THREADS` based on CPU cores
   - Consider I/O bound vs CPU bound operations
   - Monitor thread usage

3. **Caching**
   - Enable caching for development
   - Configure cache cleanup
   - Monitor cache size

4. **Documentation**
   - Choose appropriate output format
   - Configure privacy settings
   - Set up templates

5. **Logging**
   - Use appropriate log levels
   - Configure log rotation
   - Set up log handlers 