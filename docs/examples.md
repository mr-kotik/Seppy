# Seppy Examples

This document provides practical examples of using Seppy in various scenarios.

## Table of Contents

1. [Basic Examples](#basic-examples)
2. [Advanced Examples](#advanced-examples)
3. [Real-World Examples](#real-world-examples)
4. [Integration Examples](#integration-examples)
5. [Best Practices Examples](#best-practices-examples)

## Basic Examples

### Simple Script Splitting

Consider a simple Python script `calculator.py`:

```python
# calculator.py
class Calculator:
    def add(self, a, b):
        return a + b
    
    def subtract(self, a, b):
        return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

# Usage example
calc = Calculator()
print(calc.add(5, 3))
print(multiply(4, 2))
```

Split this script using Seppy:

```bash
seppy calculator.py -o calculator_modules
```

This will create:

```
calculator_modules/
├── calculator.py      # Contains Calculator class
├── multiply.py        # Contains multiply function
├── divide.py         # Contains divide function
└── docs/
    ├── calculator.md
    ├── multiply.md
    └── divide.md
```

### Using Configuration

Split a script with custom configuration:

```yaml
# config.yaml
IGNORE_PATTERNS:
  - "test_*.py"
MEMORY_LIMIT_MB: 2048
MAX_THREADS: 4
CACHE_ENABLED: true
```

```bash
seppy large_script.py -c config.yaml -o modules
```

## Advanced Examples

### Handling Complex Dependencies

Consider a script with complex dependencies:

```python
# app.py
from typing import Optional, List
import logging
import json

class DataProcessor:
    def __init__(self, logger: Optional[logging.Logger] = None):
        self.logger = logger or logging.getLogger(__name__)
        
    def process_data(self, data: List[dict]) -> dict:
        result = {}
        for item in data:
            self._validate_item(item)
            self._transform_item(item)
            result[item['id']] = item
        return result
    
    def _validate_item(self, item: dict):
        if 'id' not in item:
            raise ValueError("Item must have an id")
    
    def _transform_item(self, item: dict):
        item['processed'] = True

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

Split this script with dependency tracking:

```python
from seppy import Seppy

splitter = Seppy("app.py", config_file="config.yaml")
modules = splitter.parse_script("app.py")
splitter.save_modules("app_modules")
```

### Working with Async Code

Example of splitting async code:

```python
# async_app.py
import asyncio
import aiohttp

class AsyncDataFetcher:
    async def fetch_data(self, url: str) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.json()

async def process_urls(urls: list) -> list:
    fetcher = AsyncDataFetcher()
    tasks = [fetcher.fetch_data(url) for url in urls]
    return await asyncio.gather(*tasks)

async def main():
    urls = [
        'https://api.example.com/data1',
        'https://api.example.com/data2'
    ]
    results = await process_urls(urls)
    print(results)

if __name__ == '__main__':
    asyncio.run(main())
```

## Real-World Examples

### Web Application Refactoring

Starting with a monolithic Flask application:

```python
# app.py
from flask import Flask, request, jsonify
import sqlite3
import bcrypt

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('database.db')
    return conn

class UserManager:
    def create_user(self, username: str, password: str):
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        with get_db() as db:
            cursor = db.cursor()
            cursor.execute(
                'INSERT INTO users (username, password) VALUES (?, ?)',
                (username, hashed)
            )
            db.commit()

    def verify_user(self, username: str, password: str) -> bool:
        with get_db() as db:
            cursor = db.cursor()
            cursor.execute(
                'SELECT password FROM users WHERE username = ?',
                (username,)
            )
            result = cursor.fetchone()
            if result:
                return bcrypt.checkpw(
                    password.encode(),
                    result[0]
                )
            return False

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    user_manager = UserManager()
    try:
        user_manager.create_user(
            data['username'],
            data['password']
        )
        return jsonify({'status': 'success'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user_manager = UserManager()
    if user_manager.verify_user(
        data['username'],
        data['password']
    ):
        return jsonify({'status': 'success'}), 200
    return jsonify({'error': 'Invalid credentials'}), 401

if __name__ == '__main__':
    app.run(debug=True)
```

Split into modules using Seppy:

```bash
seppy app.py -o webapp -c webapp_config.yaml
```

## Integration Examples

### CI/CD Integration

Example GitHub Actions workflow:

```yaml
name: Split Code

on:
  push:
    paths:
      - 'src/**/*.py'

jobs:
  split-code:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install Seppy
        run: |
          python -m pip install --upgrade pip
          pip install -e .
      - name: Split Code
        run: |
          for file in src/*.py; do
            seppy "$file" -o "modules/$(basename "$file" .py)"
          done
```

### Pre-commit Hook

Example pre-commit configuration:

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: seppy-split
        name: Split large Python files
        entry: seppy
        language: python
        types: [python]
        args: [-o, modules]
```

## Best Practices Examples

### Module Organization

Example directory structure:

```
project/
├── src/
│   ├── core/
│   │   ├── __init__.py
│   │   └── large_module.py
│   ├── utils/
│   │   └── helpers.py
│   └── main.py
├── tests/
│   └── test_core.py
└── seppy.yaml
```

Seppy configuration for this project:

```yaml
# seppy.yaml
IGNORE_PATTERNS:
  - "tests/*"
  - "**/__init__.py"
MEMORY_LIMIT_MB: 2048
MAX_THREADS: 4
CACHE_ENABLED: true
REPORT_FORMAT: "md"
LOG_LEVEL: "INFO"
```

Split command:

```bash
seppy src/core/large_module.py -c seppy.yaml -o src/core/modules
```

### Documentation Generation

Example module with comprehensive docstrings:

```python
# analytics.py
"""
Analytics module for processing and analyzing data.

This module provides functionality for:
- Data processing
- Statistical analysis
- Report generation
"""

class DataAnalyzer:
    """
    Performs statistical analysis on data sets.
    
    Attributes:
        data (pd.DataFrame): The input data
        results (dict): Analysis results
    """
    
    def analyze(self, data: pd.DataFrame) -> dict:
        """
        Perform statistical analysis.
        
        Args:
            data: Input DataFrame
            
        Returns:
            Dictionary with analysis results
        """
        pass
```

Generate documentation:

```bash
seppy analytics.py -o analytics_modules
```

This will create detailed markdown documentation preserving all docstrings and adding cross-references. 