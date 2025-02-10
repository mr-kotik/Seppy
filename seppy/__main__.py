import argparse
import sys
from pathlib import Path
from rich.console import Console
from rich.logging import RichHandler
import logging

from .core import Seppy
from .config import DEFAULT_CONFIG
from .exceptions import ScriptSplitterError

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)

logger = logging.getLogger("seppy")
console = Console()

def main():
    """Основная точка входа в программу."""
    parser = argparse.ArgumentParser(
        description="Seppy - инструмент для разделения Python скриптов на модули"
    )
    parser.add_argument(
        "source_file",
        help="Путь к исходному Python файлу"
    )
    parser.add_argument(
        "-o", "--output",
        help="Директория для сохранения результатов (по умолчанию: output)",
        default="output"
    )
    parser.add_argument(
        "-c", "--config",
        help="Путь к файлу конфигурации (JSON или YAML)"
    )
    parser.add_argument(
        "-m", "--memory-limit",
        type=int,
        help="Лимит памяти в МБ"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Включить подробное логирование"
    )

    args = parser.parse_args()

    # Настройка уровня логирования
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    try:
        # Проверка существования исходного файла
        source_path = Path(args.source_file)
        if not source_path.exists():
            raise FileNotFoundError(f"Файл не найден: {args.source_file}")
        
        # Инициализация Seppy
        splitter = Seppy(
            source_file=str(source_path),
            config_file=args.config,
            memory_limit_mb=args.memory_limit
        )
        
        # Анализ и разделение скрипта
        logger.info("Начинаем анализ скрипта...")
        modules = splitter.parse_script(str(source_path))
        logger.info(f"Найдено {len(modules)} модулей")
        
        # Сохранение результатов
        output_path = Path(args.output)
        logger.info(f"Сохраняем модули в {output_path}...")
        splitter.save_modules(str(output_path))
        
        logger.info("Готово! 🎉")
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"Ошибка: {e}")
        return 1
    except ScriptSplitterError as e:
        logger.error(f"Ошибка при обработке скрипта: {e}")
        return 1
    except Exception as e:
        logger.error(f"Неожиданная ошибка: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 