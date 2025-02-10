import argparse
import sys
from pathlib import Path
from rich.console import Console
from rich.logging import RichHandler
import logging

from .core import Seppy
from .config import DEFAULT_CONFIG
from .exceptions import ScriptSplitterError

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)

logger = logging.getLogger("seppy")
console = Console()

def main():
    """Main entry point for the program."""
    parser = argparse.ArgumentParser(
        description="Seppy - A tool for splitting Python scripts into modules"
    )
    parser.add_argument(
        "source_file",
        help="Path to the source Python file"
    )
    parser.add_argument(
        "-o", "--output",
        help="Output directory (default: output)",
        default="output"
    )
    parser.add_argument(
        "-c", "--config",
        help="Path to configuration file (JSON or YAML)"
    )
    parser.add_argument(
        "-m", "--memory-limit",
        type=int,
        help="Memory limit in MB"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )

    args = parser.parse_args()

    # Configure logging level
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    try:
        # Check if source file exists
        source_path = Path(args.source_file)
        if not source_path.exists():
            raise FileNotFoundError(f"File not found: {args.source_file}")
        
        # Initialize Seppy
        splitter = Seppy(
            source_file=str(source_path),
            config_file=args.config,
            memory_limit_mb=args.memory_limit
        )
        
        # Parse and split the script
        logger.info("Starting script analysis...")
        modules = splitter.parse_script(str(source_path))
        logger.info(f"Found {len(modules)} modules")
        
        # Save results
        output_path = Path(args.output)
        logger.info(f"Saving modules to {output_path}...")
        splitter.save_modules(str(output_path))
        
        logger.info("Done! 🎉")
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"Error: {e}")
        return 1
    except ScriptSplitterError as e:
        logger.error(f"Script processing error: {e}")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 