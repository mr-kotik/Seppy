import ast
from typing import Dict, Set, Any, Tuple, Optional
from .models import ModuleInfo
from .analyzers import (
    find_used_imports,
    find_used_globals,
    extract_imports,
    analyze_complex_structures
)

def organize_imports(imports: Set[str]) -> str:
    """Organize imports into a formatted string."""
    stdlib_imports = []
    third_party_imports = []
    local_imports = []
    
    for imp in sorted(imports):
        if '.' in imp:
            module = imp.split('.')[0]
            if module.startswith('_'):
                local_imports.append(imp)
            else:
                third_party_imports.append(imp)
        else:
            stdlib_imports.append(imp)
    
    import_str = ""
    if stdlib_imports:
        import_str += "\n".join(f"import {imp}" for imp in sorted(stdlib_imports)) + "\n"
    if third_party_imports:
        if stdlib_imports:
            import_str += "\n"
        import_str += "\n".join(f"from {imp.split('.')[0]} import {'.'.join(imp.split('.')[1:])}"
                               for imp in sorted(third_party_imports)) + "\n"
    if local_imports:
        if stdlib_imports or third_party_imports:
            import_str += "\n"
        import_str += "\n".join(f"from {imp.split('.')[0]} import {'.'.join(imp.split('.')[1:])}"
                               for imp in sorted(local_imports))
    
    return import_str

def create_module_code(imports: Set[str], code: str) -> str:
    """Create module code with organized imports."""
    import_str = organize_imports(imports)
    return f"{import_str}\n\n{code}" if import_str else code

def create_module_docs(module_name: str, code: str) -> str:
    """Create documentation for a module."""
    try:
        tree = ast.parse(code)
        docstring = ast.get_docstring(tree)
        
        functions = []
        classes = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                func_doc = ast.get_docstring(node) or "No documentation available."
                functions.append(f"### Function: {node.name}\n{func_doc}")
            elif isinstance(node, ast.ClassDef):
                class_doc = ast.get_docstring(node) or "No documentation available."
                classes.append(f"### Class: {node.name}\n{class_doc}")
        
        docs = [f"# Module: {module_name}"]
        if docstring:
            docs.append(f"\n{docstring}")
        
        if functions:
            docs.append("\n## Functions\n")
            docs.extend(functions)
        
        if classes:
            docs.append("\n## Classes\n")
            docs.extend(classes)
        
        return "\n".join(docs)
    except Exception as e:
        return f"# Module: {module_name}\n\nError generating documentation: {str(e)}"

def create_complex_module(name: str, node: ast.AST, structures: Dict[str, Any]) -> str:
    """Create a module from complex code structures."""
    code_parts = []
    
    # Add imports
    if structures['imports']:
        code_parts.append(organize_imports(structures['imports']))
    
    # Add class definitions
    for class_name, class_info in structures['classes'].items():
        class_code = [f"class {class_name}:"]
        for method in class_info['methods']:
            class_code.append(f"    def {method}(self):")
            class_code.append("        pass")
        code_parts.append("\n".join(class_code))
    
    # Add function definitions
    for func_name, func_info in structures['functions'].items():
        args = ", ".join(func_info['args'])
        returns = f" -> {func_info['returns']}" if func_info['returns'] else ""
        func_code = [f"def {func_name}({args}){returns}:",
                    "    pass"]
        code_parts.append("\n".join(func_code))
    
    return "\n\n".join(code_parts) 