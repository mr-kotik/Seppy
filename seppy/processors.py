"""Documentation generation and processing functionality."""

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
    """Create documentation for a module.
    
    Args:
        module_name: Name of the module to document
        code: Source code of the module
        
    Returns:
        str: Generated markdown documentation
    """
    try:
        # Предварительная проверка кода
        try:
            tree = ast.parse(code)
        except IndentationError as e:
            # Если есть проблемы с отступами, пробуем исправить
            fixed_code = "\n".join(line.rstrip() for line in code.splitlines())
            tree = ast.parse(fixed_code)
        except SyntaxError as e:
            raise Exception(f"Syntax error in code: {str(e)}")
        
        docstring = ast.get_docstring(tree) or "No module documentation available."
        
        def format_decorator(decorator: ast.expr) -> str:
            """Format decorator node as string."""
            if isinstance(decorator, ast.Name):
                return f"@{decorator.id}"
            elif isinstance(decorator, ast.Call):
                if isinstance(decorator.func, ast.Name):
                    args = [ast.unparse(arg) for arg in decorator.args]
                    kwargs = [f"{kw.arg}={ast.unparse(kw.value)}" for kw in decorator.keywords]
                    all_args = args + kwargs
                    return f"@{decorator.func.id}({', '.join(all_args)})"
                elif isinstance(decorator.func, ast.Attribute):
                    return f"@{ast.unparse(decorator.func)}({', '.join(ast.unparse(arg) for arg in decorator.args)})"
            return f"@{ast.unparse(decorator)}"
        
        def format_body(body: list) -> str:
            """Format function/method body as string.
            
            Args:
                body: List of AST nodes representing the function body
                
            Returns:
                str: Formatted code with proper indentation
            """
            if not body:
                return "pass"
            
            def format_node(node: ast.AST, indent: int = 0) -> str:
                """Format single AST node with proper indentation."""
                indent_str = "    " * indent
                
                if isinstance(node, ast.With):
                    # Форматируем with блок
                    items = [ast.unparse(item) for item in node.items]
                    with_str = f"{indent_str}with {', '.join(items)}:"
                    body_lines = []
                    for stmt in node.body:
                        body_lines.extend(format_node(stmt, indent + 1).split('\n'))
                    return '\n'.join([with_str] + body_lines)
                    
                elif isinstance(node, ast.AsyncWith):
                    # Форматируем async with блок
                    items = [ast.unparse(item) for item in node.items]
                    with_str = f"{indent_str}async with {', '.join(items)}:"
                    body_lines = []
                    for stmt in node.body:
                        body_lines.extend(format_node(stmt, indent + 1).split('\n'))
                    return '\n'.join([with_str] + body_lines)
                    
                elif isinstance(node, ast.If):
                    # Форматируем if блок
                    if_str = f"{indent_str}if {ast.unparse(node.test)}:"
                    body_lines = []
                    for stmt in node.body:
                        body_lines.extend(format_node(stmt, indent + 1).split('\n'))
                    
                    if node.orelse:
                        body_lines.append(f"{indent_str}else:")
                        for stmt in node.orelse:
                            body_lines.extend(format_node(stmt, indent + 1).split('\n'))
                    
                    return '\n'.join([if_str] + body_lines)
                    
                elif isinstance(node, ast.For):
                    # Форматируем for блок
                    for_str = f"{indent_str}for {ast.unparse(node.target)} in {ast.unparse(node.iter)}:"
                    body_lines = []
                    for stmt in node.body:
                        body_lines.extend(format_node(stmt, indent + 1).split('\n'))
                    
                    if node.orelse:
                        body_lines.append(f"{indent_str}else:")
                        for stmt in node.orelse:
                            body_lines.extend(format_node(stmt, indent + 1).split('\n'))
                    
                    return '\n'.join([for_str] + body_lines)
                    
                elif isinstance(node, ast.AsyncFor):
                    # Форматируем async for блок
                    for_str = f"{indent_str}async for {ast.unparse(node.target)} in {ast.unparse(node.iter)}:"
                    body_lines = []
                    for stmt in node.body:
                        body_lines.extend(format_node(stmt, indent + 1).split('\n'))
                    
                    if node.orelse:
                        body_lines.append(f"{indent_str}else:")
                        for stmt in node.orelse:
                            body_lines.extend(format_node(stmt, indent + 1).split('\n'))
                    
                    return '\n'.join([for_str] + body_lines)
                    
                elif isinstance(node, ast.Try):
                    # Форматируем try блок
                    lines = [f"{indent_str}try:"]
                    for stmt in node.body:
                        lines.extend(format_node(stmt, indent + 1).split('\n'))
                    
                    for handler in node.handlers:
                        if handler.type:
                            if handler.name:
                                lines.append(f"{indent_str}except {ast.unparse(handler.type)} as {handler.name}:")
                            else:
                                lines.append(f"{indent_str}except {ast.unparse(handler.type)}:")
                        else:
                            lines.append(f"{indent_str}except:")
                        
                        for stmt in handler.body:
                            lines.extend(format_node(stmt, indent + 1).split('\n'))
                    
                    if node.orelse:
                        lines.append(f"{indent_str}else:")
                        for stmt in node.orelse:
                            lines.extend(format_node(stmt, indent + 1).split('\n'))
                    
                    if node.finalbody:
                        lines.append(f"{indent_str}finally:")
                        for stmt in node.finalbody:
                            lines.extend(format_node(stmt, indent + 1).split('\n'))
                    
                    return '\n'.join(lines)
                    
                elif isinstance(node, ast.While):
                    # Форматируем while блок
                    while_str = f"{indent_str}while {ast.unparse(node.test)}:"
                    body_lines = []
                    for stmt in node.body:
                        body_lines.extend(format_node(stmt, indent + 1).split('\n'))
                    
                    if node.orelse:
                        body_lines.append(f"{indent_str}else:")
                        for stmt in node.orelse:
                            body_lines.extend(format_node(stmt, indent + 1).split('\n'))
                    
                    return '\n'.join([while_str] + body_lines)
                    
                else:
                    # Для остальных узлов используем стандартное форматирование
                    return f"{indent_str}{ast.unparse(node)}"
            
            # Форматируем каждый узел в теле функции
            formatted_lines = []
            for node in body:
                formatted_lines.append(format_node(node))
            
            return '\n'.join(formatted_lines)
        
        # Собираем импорты
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for name in node.names:
                    imports.append(f"`{name.name}`" + (f" as `{name.asname}`" if name.asname else ""))
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ''
                for name in node.names:
                    if name.name == '*':
                        imports.append(f"from `{module}` import *")
                    else:
                        imports.append(f"from `{module}` import `{name.name}`" + 
                                    (f" as `{name.asname}`" if name.asname else ""))
        
        # Собираем функции
        functions = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if not any(isinstance(parent, ast.ClassDef) for parent in ast.walk(tree) 
                          if hasattr(parent, 'body') and node in parent.body):
                    func_doc = ast.get_docstring(node) or "No documentation available."
                    func_type = "Async Function" if isinstance(node, ast.AsyncFunctionDef) else "Function"
                    
                    # Получаем аргументы функции
                    args = []
                    for arg in node.args.args:
                        arg_str = f"`{arg.arg}`"
                        if arg.annotation:
                            arg_str += f": `{ast.unparse(arg.annotation)}`"
                        args.append(arg_str)
                    
                    # Получаем возвращаемый тип
                    returns = f" -> `{ast.unparse(node.returns)}`" if node.returns else ""
                    
                    # Получаем декораторы
                    decorators = [format_decorator(d) for d in node.decorator_list]
                    
                    # Получаем тело функции
                    body = format_body(node.body)
                    
                    func_info = [
                        f"### {func_type}: `{node.name}`",
                        "",
                        "**Decorators:**" if decorators else None,
                        "\n".join(f"- `{d}`" for d in decorators) if decorators else None,
                        "",
                        "**Signature:**",
                        f"```python\n{node.name}({', '.join(args)}){returns}\n```",
                        "",
                        "**Documentation:**",
                        func_doc,
                        "",
                        "**Implementation:**" if body != "pass" else None,
                        f"```python\n{body}\n```" if body != "pass" else None
                    ]
                    functions.append("\n".join(filter(None, func_info)))
        
        # Собираем классы
        classes = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_doc = ast.get_docstring(node) or "No documentation available."
                
                # Получаем базовые классы
                bases = [ast.unparse(base) for base in node.bases]
                bases_str = f"({', '.join(f'`{base}`' for base in bases)})" if bases else ""
                
                # Получаем декораторы класса
                class_decorators = [format_decorator(d) for d in node.decorator_list]
                
                # Собираем методы
                methods = []
                for child in node.body:
                    if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        method_doc = ast.get_docstring(child) or "No documentation available."
                        method_type = "Async Method" if isinstance(child, ast.AsyncFunctionDef) else "Method"
                        
                        # Получаем аргументы метода
                        args = []
                        for arg in child.args.args:
                            arg_str = f"`{arg.arg}`"
                            if arg.annotation:
                                arg_str += f": `{ast.unparse(arg.annotation)}`"
                            args.append(arg_str)
                        
                        # Получаем возвращаемый тип
                        returns = f" -> `{ast.unparse(child.returns)}`" if child.returns else ""
                        
                        # Получаем декораторы метода
                        method_decorators = [format_decorator(d) for d in child.decorator_list]
                        
                        # Получаем тело метода
                        body = format_body(child.body)
                        
                        method_info = [
                            f"#### {method_type}: `{child.name}`",
                            "",
                            "**Decorators:**" if method_decorators else None,
                            "\n".join(f"- `{d}`" for d in method_decorators) if method_decorators else None,
                            "",
                            "**Signature:**",
                            f"```python\n{child.name}({', '.join(args)}){returns}\n```",
                            "",
                            "**Documentation:**",
                            method_doc,
                            "",
                            "**Implementation:**" if body != "pass" else None,
                            f"```python\n{body}\n```" if body != "pass" else None
                        ]
                        methods.append("\n".join(filter(None, method_info)))
                
                class_info = [
                    f"### Class: `{node.name}`{bases_str}",
                    "",
                    "**Decorators:**" if class_decorators else None,
                    "\n".join(f"- `{d}`" for d in class_decorators) if class_decorators else None,
                    "",
                    "**Documentation:**",
                    class_doc,
                    "",
                    "**Methods:**" if methods else None,
                    "\n\n".join(methods) if methods else None
                ]
                classes.append("\n".join(filter(None, class_info)))
        
        # Собираем все части документации
        docs = [
            f"# Module: `{module_name}`",
            "",
            "## Description",
            docstring,
            "",
            "## Imports" if imports else None,
            "\n".join(f"- {imp}" for imp in imports) if imports else None,
            "",
            "## Functions" if functions else None,
            "\n\n".join(functions) if functions else None,
            "",
            "## Classes" if classes else None,
            "\n\n".join(classes) if classes else None
        ]
        
        return "\n".join(filter(None, docs))
        
    except Exception as e:
        # В случае ошибки возвращаем базовую документацию с информацией об ошибке
        error_docs = [
            f"# Module: `{module_name}`",
            "",
            "## Error",
            f"Failed to generate complete documentation: {str(e)}",
            "",
            "## Basic Information",
            "This module is part of the codebase but detailed documentation could not be generated.",
            "Please check the source code directly for more information.",
            "",
            "### Error Details",
            "```python",
            str(e.__class__.__name__),
            str(e),
            "```"
        ]
        return "\n".join(error_docs)

def create_complex_module(name: str, node: ast.AST, structures: Dict[str, Any]) -> str:
    """Create a module from complex code structures."""
    code_parts = []
    
    # Add type aliases and generic types
    for alias_name, alias_type in structures.get('type_aliases', {}).items():
        code_parts.append(f"{alias_name}: {alias_type}")
    
    for type_name, type_def in structures.get('generic_types', {}).items():
        code_parts.append(f"{type_name} = {type_def}")
    
    # Add type variables
    for var_name, bounds in structures.get('type_vars', {}).items():
        if bounds:
            code_parts.append(f"{var_name} = TypeVar('{var_name}', {', '.join(bounds)})")
        else:
            code_parts.append(f"{var_name} = TypeVar('{var_name}')")
    
    # Add constants
    for const_name, const_value in structures.get('constants', {}).items():
        code_parts.append(f"{const_name} = {const_value}")
    
    # Add imports
    if structures['imports']:
        code_parts.append(organize_imports(structures['imports']))
    
    # Add global and nonlocal declarations
    for global_var in structures.get('global_vars', set()):
        code_parts.append(f"global {global_var}")
    
    for nonlocal_var in structures.get('nonlocal_vars', set()):
        code_parts.append(f"nonlocal {nonlocal_var}")
    
    # Add assignments
    for assignment in structures.get('assignments', []):
        code_parts.append(f"{assignment['target']} = {assignment['value']}")
    
    # Add walrus operators
    for walrus in structures.get('walrus_ops', []):
        code_parts.append(f"({walrus['target']} := {walrus['value']})")
    
    # Add original source code or reconstruct it
    if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
        # Get the source lines for the node
        source_lines = ast.get_source_segment(structures.get('source', ''), node)
        if source_lines:
            # Add decorators if they're not in the source
            decorators = []
            if isinstance(node, ast.ClassDef):
                decorators = structures['classes'].get(node.name, {}).get('decorators', [])
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                func_dict = structures['async_functions' if isinstance(node, ast.AsyncFunctionDef) else 'functions']
                decorators = func_dict.get(node.name, {}).get('decorators', [])
            
            if decorators and not any(d in source_lines for d in decorators):
                code_parts.extend(f"@{d}" for d in decorators)
            
            code_parts.append(source_lines)
            
            # Add nested classes after the main class
            if isinstance(node, ast.ClassDef):
                for nested_name, nested_struct in structures.get('nested_classes', {}).items():
                    nested_code = create_complex_module(nested_name, node, nested_struct)
                    code_parts.append("\n" + "\n".join("    " + line for line in nested_code.split("\n")))
        else:
            # Fallback to reconstructing the code
            if isinstance(node, ast.ClassDef):
                class_info = structures['classes'][node.name]
                # Add decorators
                for decorator in class_info.get('decorators', []):
                    code_parts.append(f"@{decorator}")
                
                # Add class definition with metaclass
                bases = class_info.get('bases', [])
                metaclass = class_info.get('metaclass')
                if metaclass:
                    bases_str = f"({', '.join(bases)}, metaclass={metaclass})" if bases else f"(metaclass={metaclass})"
                else:
                    bases_str = f"({', '.join(bases)})" if bases else ""
                
                # Add Protocol marker if needed
                if class_info.get('is_protocol'):
                    code_parts.append("@runtime_checkable" if structures['protocols'].get(node.name, {}).get('runtime_checkable') else "")
                
                code_parts.append(f"class {node.name}{bases_str}:")
                
                # Add docstring
                if class_info.get('docstring'):
                    code_parts.append(f'    """{class_info["docstring"]}"""')
                
                # Add dataclass fields
                if class_info.get('is_dataclass'):
                    for field_name, field_info in structures.get('dataclasses', {}).items():
                        field_str = f"    {field_name}: {field_info['type']}"
                        if field_info.get('default'):
                            field_str += f" = {field_info['default']}"
                        if field_info.get('metadata'):
                            metadata_str = ", ".join(f"{k}={v}" for k, v in field_info['metadata'].items())
                            field_str += f" = field({metadata_str})"
                        code_parts.append(field_str)
                
                # Add class variables
                for var in class_info.get('class_vars', []):
                    if var.get('value'):
                        code_parts.append(f"    {var['name']}: {var['type']} = {var['value']}")
                    else:
                        code_parts.append(f"    {var['name']}: {var['type']}")
                
                # Add methods
                for method in class_info.get('methods', []):
                    # Add method decorators
                    for decorator in method.get('decorators', []):
                        code_parts.append(f"    @{decorator}")
                    
                    # Get method source or reconstruct
                    if method.get('node'):
                        method_source = ast.get_source_segment(structures.get('source', ''), method['node'])
                        if method_source:
                            code_parts.append("\n".join("    " + line for line in method_source.split("\n")))
                            continue
                    
                    # Reconstruct method if source not available
                    args = ["self"] + method.get('args', [])
                    args_str = ", ".join(args)
                    returns = f" -> {method['returns']}" if method.get('returns') else ""
                    code_parts.append(f"    def {method['name']}({args_str}){returns}:")
                    
                    if method.get('docstring'):
                        code_parts.append(f'        """{method["docstring"]}"""')
                    
                    if method.get('body'):
                        for line in [ast.unparse(stmt) for stmt in method['body']]:
                            code_parts.append(f"        {line}")
                    else:
                        code_parts.append(f"        raise NotImplementedError")
                
                # Add async methods
                for method in class_info.get('async_methods', []):
                    # Add method decorators
                    for decorator in method.get('decorators', []):
                        code_parts.append(f"    @{decorator}")
                    
                    # Get method source or reconstruct
                    if method.get('node'):
                        method_source = ast.get_source_segment(structures.get('source', ''), method['node'])
                        if method_source:
                            code_parts.append("\n".join("    " + line for line in method_source.split("\n")))
                            continue
                    
                    # Reconstruct method if source not available
                    args = ["self"] + method.get('args', [])
                    args_str = ", ".join(args)
                    returns = f" -> {method['returns']}" if method.get('returns') else ""
                    code_parts.append(f"    async def {method['name']}({args_str}){returns}:")
                    
                    if method.get('docstring'):
                        code_parts.append(f'        """{method["docstring"]}"""')
                    
                    if method.get('body'):
                        for line in [ast.unparse(stmt) for stmt in method['body']]:
                            code_parts.append(f"        {line}")
                    else:
                        code_parts.append(f"        raise NotImplementedError")
                
                # Add nested classes
                for nested_name, nested_struct in structures.get('nested_classes', {}).items():
                    nested_code = create_complex_module(nested_name, node, nested_struct)
                    code_parts.append("\n" + "\n".join("    " + line for line in nested_code.split("\n")))
            else:
                # Function or async function
                func_dict = structures['async_functions' if isinstance(node, ast.AsyncFunctionDef) else 'functions']
                func_info = func_dict[node.name]
                
                # Add decorators
                for decorator in func_info.get('decorators', []):
                    code_parts.append(f"@{decorator}")
                
                # Get function source or reconstruct
                if func_info.get('node'):
                    body_source = ast.get_source_segment(structures.get('source', ''), func_info['node'])
                    if body_source:
                        code_parts.append(body_source)
                        
                        # Add nested functions with original source
                        for nested_name, nested_info in func_info.get('nested_functions', {}).items():
                            if nested_info.get('node'):
                                nested_source = ast.get_source_segment(structures.get('source', ''), nested_info['node'])
                                if nested_source:
                                    code_parts.append("\n" + nested_source)
                        return "\n".join(code_parts)
                
                # Reconstruct function if source not available
                async_prefix = "async " if func_info.get('is_async', False) else ""
                args_str = ", ".join(func_info.get('args', []))
                returns = func_info.get('returns', '')
                code_parts.append(f"{async_prefix}def {node.name}({args_str}){returns}:")
                
                if func_info.get('docstring'):
                    code_parts.append(f'    """{func_info["docstring"]}"""')
                
                if func_info.get('body'):
                    for line in [ast.unparse(stmt) for stmt in func_info['body']]:
                        code_parts.append(f"    {line}")
                else:
                    code_parts.append(f"    raise NotImplementedError")
                
                # Add nested functions
                for nested_name, nested_info in func_info.get('nested_functions', {}).items():
                    code_parts.append("")
                    # Add nested function decorators
                    if nested_info.get('decorators'):
                        for decorator in nested_info['decorators']:
                            code_parts.append(f"    @{decorator}")
                    
                    # Get nested function source or reconstruct
                    if nested_info.get('node'):
                        nested_source = ast.get_source_segment(structures.get('source', ''), nested_info['node'])
                        if nested_source:
                            code_parts.append("\n".join("    " + line for line in nested_source.split("\n")))
                            continue
                    
                    # Reconstruct nested function
                    async_prefix = "async " if nested_info.get('is_async', False) else ""
                    args_str = ", ".join(nested_info.get('args', []))
                    returns = nested_info.get('returns', '')
                    code_parts.append(f"    {async_prefix}def {nested_name}({args_str}){returns}:")
                    
                    if nested_info.get('docstring'):
                        code_parts.append(f'        """{nested_info["docstring"]}"""')
                    
                    if nested_info.get('body'):
                        for line in [ast.unparse(stmt) for stmt in nested_info['body']]:
                            code_parts.append(f"        {line}")
                    else:
                        code_parts.append(f"        raise NotImplementedError")
    
    # Add comprehensions
    for comp in structures.get('comprehensions', []):
        code_parts.append(comp['code'])
    
    # Add generators
    for gen in structures.get('generators', []):
        code_parts.append(gen['code'])
    
    # Add lambda functions
    for lambda_func in structures.get('lambda_funcs', []):
        args_str = ", ".join(lambda_func['args'])
        code_parts.append(f"lambda {args_str}: {lambda_func['body']}")
    
    # Add match statements
    for match_case in structures.get('match_cases', []):
        code_parts.append(f"match {match_case['subject']}:")
        for case in match_case['cases']:
            case_line = f"    case {case['pattern']}"
            if case['guard']:
                case_line += f" if {case['guard']}"
            code_parts.append(case_line + ":")
            for line in case['body']:
                code_parts.append(f"        {line}")
    
    # Add with blocks
    for with_block in structures.get('with_blocks', []):
        items_str = ", ".join(with_block['items'])
        code_parts.append(f"with {items_str}:")
        for body_line in with_block['body']:
            code_parts.append(f"    {body_line}")
    
    # Add async with blocks
    for with_block in structures.get('async_with', []):
        items_str = ", ".join(with_block['items'])
        code_parts.append(f"async with {items_str}:")
        for body_line in with_block['body']:
            code_parts.append(f"    {body_line}")
    
    # Add async for loops
    for for_loop in structures.get('async_for', []):
        code_parts.append(f"async for {for_loop['target']} in {for_loop['iter']}:")
        for body_line in for_loop['body']:
            code_parts.append(f"    {body_line}")
    
    # Add try blocks
    for try_block in structures.get('try_blocks', []):
        code_parts.append("try:")
        for body_line in try_block['body']:
            code_parts.append(f"    {body_line}")
        
        for handler in try_block['handlers']:
            if handler['type']:
                code_parts.append(f"except {handler['type']} as {handler['name']}:")
            else:
                code_parts.append("except:")
            for line in handler['body']:
                code_parts.append(f"    {line}")
        
        if try_block.get('else_body'):
            code_parts.append("else:")
            for line in try_block['else_body']:
                code_parts.append(f"    {line}")
        
        if try_block.get('finally_body'):
            code_parts.append("finally:")
            for line in try_block['finally_body']:
                code_parts.append(f"    {line}")
    
    # Add yield expressions
    for yield_expr in structures.get('yield_exprs', []):
        code_parts.append(yield_expr['expr'])
    
    # Add await expressions
    for await_expr in structures.get('await_exprs', []):
        code_parts.append(await_expr['expr'])
    
    # Add f-strings
    for f_string in structures.get('f_strings', []):
        code_parts.append(f_string['code'])
    
    # Add type comments
    for node_str, type_comment in structures.get('type_comments', {}).items():
        code_parts.append(f"{node_str}  # type: {type_comment}")
    
    return "\n".join(code_parts)

class DocumentationGenerator:
    """Generator for module documentation."""
    
    def __init__(self, module_info: ModuleInfo):
        self.module_info = module_info
        
    def generate_markdown(self) -> str:
        """Generate markdown documentation."""
        doc_parts = []
        
        # Module header
        doc_parts.append(f"# {self.module_info.name}\n")
        
        # Module docstring
        if self.module_info.docstring:
            doc_parts.append(self.module_info.docstring + "\n")
            
        # Imports section
        if self.module_info.imports:
            doc_parts.append("## Imports\n")
            for imp in sorted(self.module_info.imports):
                doc_parts.append(f"- `{imp}`")
            doc_parts.append("")
            
        # Classes section
        if self.module_info.classes:
            doc_parts.append("## Classes\n")
            for class_name in sorted(self.module_info.classes):
                doc_parts.append(f"### {class_name}\n")
                # Add class documentation here
                
        # Functions section
        if self.module_info.functions:
            doc_parts.append("## Functions\n")
            for func_name in sorted(self.module_info.functions):
                doc_parts.append(f"### {func_name}\n")
                # Add function documentation here
                
        # Async functions section
        if self.module_info.async_functions:
            doc_parts.append("## Async Functions\n")
            for func_name in sorted(self.module_info.async_functions):
                doc_parts.append(f"### {func_name}\n")
                # Add async function documentation here
                
        return "\n".join(doc_parts)
        
    def _format_signature(self, node: ast.AST) -> str:
        """Format function or method signature."""
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            args = []
            for arg in node.args.args:
                annotation = f": {ast.unparse(arg.annotation)}" if arg.annotation else ""
                args.append(f"{arg.arg}{annotation}")
            
            returns = f" -> {ast.unparse(node.returns)}" if node.returns else ""
            async_prefix = "async " if isinstance(node, ast.AsyncFunctionDef) else ""
            
            return f"{async_prefix}def {node.name}({', '.join(args)}){returns}"
        return ""
        
    def _format_decorators(self, node: ast.AST) -> str:
        """Format decorators for a node."""
        if hasattr(node, 'decorator_list'):
            return "\n".join(f"@{ast.unparse(d)}" for d in node.decorator_list)
        return "" 