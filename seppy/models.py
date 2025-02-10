from dataclasses import dataclass, field
from typing import Set, Optional, List

@dataclass
class ModuleInfo:
    """Information about a module."""
    name: str
    code: str
    imports: Set[str]
    global_vars: Set[str]
    functions: Set[str]
    classes: Set[str]
    async_functions: Set[str] = field(default_factory=set)
    dependencies: Set[str] = field(default_factory=set)
    docstring: Optional[str] = None
    decorators: Set[str] = field(default_factory=set)
    docs: str = ""

@dataclass
class CacheData:
    """Class for storing cached data."""
    docs: str
    hash: str

@dataclass
class ProcessingStats:
    """Statistics about script processing."""
    total_modules: int = 0
    processed_modules: int = 0
    failed_modules: int = 0
    cached_modules: int = 0
    processing_time: float = 0.0
    memory_usage: List[int] = field(default_factory=list)
    errors: List[str] = field(default_factory=list) 