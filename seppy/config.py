from typing import List
from typing_extensions import TypedDict

class SeppyConfig(TypedDict):
    """Configuration type definition."""
    IGNORE_PATTERNS: List[str]
    MEMORY_LIMIT_MB: int
    MAX_THREADS: int
    CACHE_ENABLED: bool
    REPORT_FORMAT: str
    LOG_LEVEL: str

DEFAULT_CONFIG: SeppyConfig = {
    "IGNORE_PATTERNS": ["*.pyc", "__pycache__/*", ".*"],
    "MEMORY_LIMIT_MB": 1024,
    "MAX_THREADS": 4,
    "CACHE_ENABLED": True,
    "REPORT_FORMAT": "md",
    "LOG_LEVEL": "INFO"
}

# Constants for file operations
MAX_LINES_PER_READ = 250
CACHE_DIR_NAME = '.seppy_cache'
DEFAULT_ENCODING = 'utf-8'

# Constants for memory management
MIN_MEMORY_LIMIT = 256  # MB
MAX_MEMORY_LIMIT = 8192  # MB
MEMORY_CHECK_INTERVAL = 60  # seconds

# Constants for parallel processing
MIN_THREADS = 1
MAX_THREADS = 16
DEFAULT_THREAD_COUNT = 4

# Constants for caching
CACHE_VERSION = '1.0.0'
MAX_CACHE_SIZE = 1024 * 1024 * 1024  # 1 GB
CACHE_CLEANUP_THRESHOLD = 0.9  # 90% 