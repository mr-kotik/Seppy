import time
import logging
from functools import wraps
from rich.logging import RichHandler
from rich.console import Console

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)

logger = logging.getLogger("seppy")
console = Console()

def time_operation(operation_name: str):
    """Decorator for measuring operation execution time."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            elapsed_time = end_time - start_time
            logger.info(f"Operation '{operation_name}' took {elapsed_time:.2f} seconds")
            return result
        return wrapper
    return decorator 