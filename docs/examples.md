# Usage Examples

This document provides practical examples of using Seppy for code analysis and documentation generation.

## Basic Usage

### Analyzing a Single File

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

### Working with Multiple Files

```python
import os
from seppy import Seppy

def analyze_directory(directory: str):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                analyzer = Seppy(file_path)
                analyzer.generate_docs(f"docs/{file}")

analyze_directory("src/")
```

## Advanced Examples

### Class Analysis

```python
# example_classes.py
from dataclasses import dataclass
from typing import Optional, List

@dataclass
class User:
    name: str
    age: int
    email: Optional[str] = None

class DataProcessor:
    def __init__(self):
        self.data = []
    
    def process_data(self, items: List[dict]) -> List[dict]:
        return [self._transform_item(item) for item in items]
    
    def _transform_item(self, item: dict):
        item['processed'] = True
        return item

class DataWriter:
    def save_json(self, data: dict, filename: str):
        with open(filename, 'w') as f:
            json.dump(data, f)

def main():
    processor = DataProcessor()
    writer = DataWriter()
    data = [{'id': 1}, {'id': 2}]
    processed = processor.process_data(data)
    writer.save_json(processed, 'output.json')

if __name__ == '__main__':
    main()
```

### Async Code Analysis

```python
# async_example.py
import asyncio
import aiohttp
from typing import List, Dict

class AsyncDataFetcher:
    async def fetch_data(self, url: str) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.json()
    
    async def fetch_multiple(self, urls: List[str]) -> List[dict]:
        tasks = [self.fetch_data(url) for url in urls]
        return await asyncio.gather(*tasks)

async def process_urls(urls: List[str]) -> List[Dict]:
    fetcher = AsyncDataFetcher()
    results = await fetcher.fetch_multiple(urls)
    return [{'url': url, 'data': data} for url, data in zip(urls, results)]

async def main():
    urls = [
        'https://api.example.com/data/1',
        'https://api.example.com/data/2'
    ]
    results = await process_urls(urls)
    print(f"Processed {len(results)} URLs")

if __name__ == '__main__':
    asyncio.run(main())
```

### Type Hints and Protocols

```python
# type_examples.py
from typing import Protocol, TypeVar, Generic, List
from dataclasses import dataclass

T = TypeVar('T')

class Processor(Protocol):
    def process(self, data: T) -> T:
        ...

@dataclass
class ProcessingResult(Generic[T]):
    input_data: T
    output_data: T
    success: bool = True

class NumberProcessor:
    def process(self, data: int) -> int:
        return data * 2

class TextProcessor:
    def process(self, data: str) -> str:
        return data.upper()

def process_items(processor: Processor[T], items: List[T]) -> List[ProcessingResult[T]]:
    results = []
    for item in items:
        try:
            output = processor.process(item)
            results.append(ProcessingResult(item, output))
        except Exception:
            results.append(ProcessingResult(item, item, success=False))
    return results

# Usage
numbers = [1, 2, 3, 4, 5]
number_processor = NumberProcessor()
number_results = process_items(number_processor, numbers)

texts = ["hello", "world"]
text_processor = TextProcessor()
text_results = process_items(text_processor, texts)
```

### Context Managers

```python
# context_examples.py
from typing import Optional
from contextlib import contextmanager
import time

class ResourceManager:
    def __init__(self, name: str):
        self.name = name
        self.in_use = False
    
    def acquire(self):
        self.in_use = True
        print(f"Resource {self.name} acquired")
    
    def release(self):
        self.in_use = False
        print(f"Resource {self.name} released")
    
    @contextmanager
    def resource_context(self):
        try:
            self.acquire()
            yield self
        finally:
            self.release()

class AsyncResourceManager:
    def __init__(self, name: str):
        self.name = name
        self.in_use = False
    
    async def __aenter__(self):
        self.in_use = True
        print(f"Async resource {self.name} acquired")
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.in_use = False
        print(f"Async resource {self.name} released")

# Usage
def main():
    # Synchronous context manager
    manager = ResourceManager("DB Connection")
    with manager.resource_context():
        print("Working with resource...")
        time.sleep(1)
    
    # Multiple context managers
    manager1 = ResourceManager("Cache")
    manager2 = ResourceManager("File")
    with manager1.resource_context(), manager2.resource_context():
        print("Working with multiple resources...")
        time.sleep(1)

async def async_main():
    # Async context manager
    async with AsyncResourceManager("API Connection") as manager:
        print("Working with async resource...")
        await asyncio.sleep(1)

if __name__ == '__main__':
    main()
    asyncio.run(async_main())
```

## Configuration Examples

### Custom Configuration

```python
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

```python
from seppy import Seppy

analyzer = Seppy("example.py", config_file="config.yaml")
analyzer.generate_docs("docs/")
```

## Error Handling

```python
from seppy import Seppy, ParseError, ConfigError

try:
    analyzer = Seppy("example.py", config_file="config.yaml")
    analyzer.generate_docs("docs/")
except ParseError as e:
    print(f"Failed to parse code: {e}")
except ConfigError as e:
    print(f"Invalid configuration: {e}")
except Exception as e:
    print(f"Unexpected error: {e}") 