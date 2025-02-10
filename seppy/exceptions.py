class ScriptSplitterError(Exception):
    """Base class for ScriptSplitter errors."""
    pass

class ParseError(ScriptSplitterError):
    """Error during code parsing."""
    pass

class ModuleProcessingError(ScriptSplitterError):
    """Error during module processing."""
    pass

class CacheError(ScriptSplitterError):
    """Error during cache operations."""
    pass 