import ast
from typing import Dict, Set, Any, Optional, List, Tuple
from .models import ModuleInfo

def find_used_imports(node: ast.AST, all_imports: Set[str]) -> Set[str]:
    """Find imports that are actually used in the code."""
    used_imports = set()
    for node in ast.walk(node):
        if isinstance(node, ast.Name) and node.id in all_imports:
            used_imports.add(node.id)
    return used_imports

def find_used_globals(node: ast.AST, global_vars: Set[str]) -> Set[str]:
    """Find global variables that are used in the code."""
    used_globals = set()
    for node in ast.walk(node):
        if isinstance(node, ast.Name) and node.id in global_vars:
            used_globals.add(node.id)
    return used_globals

def extract_imports(tree: ast.AST, *nodes) -> Set[str]:
    """Extract all imports from AST nodes."""
    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for name in node.names:
                imports.add(name.name)
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            for name in node.names:
                if name.name == "*":
                    imports.add(f"{module}.*")
                else:
                    imports.add(f"{module}.{name.name}")
    return imports

def get_parent_function_or_class(node: ast.AST, tree: ast.AST) -> Optional[str]:
    """Get the name of the parent function or class for a given node."""
    for parent in ast.walk(tree):
        if isinstance(parent, (ast.FunctionDef, ast.ClassDef)):
            for child in ast.walk(parent):
                if child == node:
                    return parent.name
    return None

def analyze_complex_structures(node: ast.AST, source_code: str = '') -> Dict[str, Any]:
    """Analyze complex code structures like nested classes and functions."""
    structures = {
        'imports': set(),
        'globals': set(),
        'functions': {},
        'classes': {},
        'async_functions': {},
        'decorators': set(),
        'source': source_code,
        'assignments': [],
        'constants': {},
        'type_aliases': {},
        'nested_classes': {},
        'nested_functions': {},
        'comprehensions': [],
        'try_blocks': [],
        'with_blocks': [],
        'match_cases': [],      # Python 3.10+ match statements
        'annotations': {},      # Type annotations
        'dataclasses': {},      # Dataclass fields
        'protocols': {},        # Protocol definitions
        'generators': [],       # Generator expressions
        'lambda_funcs': [],     # Lambda functions
        'async_with': [],       # Async with blocks
        'async_for': [],        # Async for loops
        'type_vars': {},        # TypeVar definitions
        'generic_types': {},    # Generic type aliases
        'property_decorators': set(),  # Property decorators
        'abstract_methods': set(),     # Abstract methods
        'static_methods': set(),       # Static methods
        'class_methods': set(),        # Class methods
        'global_vars': set(),          # Global variables
        'nonlocal_vars': set(),        # Nonlocal variables
        'yield_exprs': [],             # Yield expressions
        'await_exprs': [],             # Await expressions
        'f_strings': [],               # f-strings
        'walrus_ops': [],             # Assignment expressions (:=)
        'type_comments': {},           # Type comments
        'decorators_with_args': {}     # Decorators with arguments
    }
    
    # Analyze imports
    for n in ast.walk(node):
        if isinstance(n, ast.Import):
            for name in n.names:
                alias = f" as {name.asname}" if name.asname else ""
                structures['imports'].add(f"import {name.name}{alias}")
        elif isinstance(n, ast.ImportFrom):
            module = n.module or ''
            for name in n.names:
                alias = f" as {name.asname}" if name.asname else ""
                if name.name == '*':
                    structures['imports'].add(f"from {module} import *")
                else:
                    structures['imports'].add(f"from {module} import {name.name}{alias}")
    
    # Analyze decorators
    def extract_decorator(decorator: ast.expr) -> str:
        if isinstance(decorator, ast.Name):
            return decorator.id
        elif isinstance(decorator, ast.Call):
            if isinstance(decorator.func, ast.Name):
                args = [ast.unparse(arg) for arg in decorator.args]
                kwargs = [f"{kw.arg}={ast.unparse(kw.value)}" for kw in decorator.keywords]
                all_args = args + kwargs
                return f"{decorator.func.id}({', '.join(all_args)})"
            elif isinstance(decorator.func, ast.Attribute):
                return f"{ast.unparse(decorator.func)}({', '.join(ast.unparse(arg) for arg in decorator.args)})"
        elif isinstance(decorator, ast.Attribute):
            return ast.unparse(decorator)
        return ast.unparse(decorator)
    
    # Analyze type aliases and constants
    for n in ast.walk(node):
        if isinstance(n, ast.AnnAssign) and isinstance(n.target, ast.Name):
            if n.simple:
                structures['type_aliases'][n.target.id] = ast.unparse(n.annotation)
                # Check for generic types
                if isinstance(n.annotation, ast.Subscript):
                    structures['generic_types'][n.target.id] = ast.unparse(n.annotation)
        elif isinstance(n, ast.Assign):
            for target in n.targets:
                if isinstance(target, ast.Name):
                    if target.id.isupper():
                        structures['constants'][target.id] = ast.unparse(n.value)
                    else:
                        structures['assignments'].append({
                            'target': target.id,
                            'value': ast.unparse(n.value)
                        })
        elif isinstance(n, ast.NamedExpr):  # Walrus operator
            structures['walrus_ops'].append({
                'target': ast.unparse(n.target),
                'value': ast.unparse(n.value)
            })
    
    # Analyze type variables and protocols
    for n in ast.walk(node):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name):
            if n.func.id == 'TypeVar':
                if n.args:
                    name = ast.unparse(n.args[0])
                    bounds = [ast.unparse(arg) for arg in n.args[1:]]
                    structures['type_vars'][name] = bounds
            elif n.func.id in ('Protocol', 'runtime_checkable'):
                if isinstance(n.parent, ast.ClassDef):
                    structures['protocols'][n.parent.name] = {
                        'runtime_checkable': n.func.id == 'runtime_checkable',
                        'methods': []
                    }
    
    # Analyze functions and async functions
    for n in ast.walk(node):
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
            is_async = isinstance(n, ast.AsyncFunctionDef)
            args = []
            
            # Process arguments
            if n.args.args:
                for arg in n.args.args:
                    try:
                        annotation = f": {ast.unparse(arg.annotation)}" if arg.annotation else ""
                        args.append(f"{arg.arg}{annotation}")
                    except Exception:
                        args.append(arg.arg)
            
            # Process kwargs
            if n.args.kwarg:
                try:
                    kwarg_ann = f": {ast.unparse(n.args.kwarg.annotation)}" if n.args.kwarg.annotation else ""
                    args.append(f"**{n.args.kwarg.arg}{kwarg_ann}")
                except Exception:
                    args.append(f"**{n.args.kwarg.arg}")
            
            # Process varargs
            if n.args.vararg:
                try:
                    vararg_ann = f": {ast.unparse(n.args.vararg.annotation)}" if n.args.vararg.annotation else ""
                    args.append(f"*{n.args.vararg.arg}{vararg_ann}")
                except Exception:
                    args.append(f"*{n.args.vararg.arg}")
            
            # Process defaults
            if n.args.defaults:
                args_with_defaults = list(zip(reversed(n.args.args[-len(n.args.defaults):]), reversed(n.args.defaults)))
                for arg, default in args_with_defaults:
                    try:
                        default_str = ast.unparse(default)
                        arg_name = arg.arg
                        # Find the argument in the args list and update it
                        for i, existing_arg in enumerate(args):
                            if existing_arg.startswith(arg_name):
                                args[i] = f"{existing_arg}={default_str}"
                                break
                    except Exception:
                        continue
            
            # Process return annotation
            try:
                returns = f" -> {ast.unparse(n.returns)}" if n.returns else ""
            except Exception:
                returns = ""
            
            # Process decorators
            try:
                decorators = [extract_decorator(d) for d in n.decorator_list]
                # Analyze special decorators
                for decorator in n.decorator_list:
                    if isinstance(decorator, ast.Name):
                        if decorator.id == 'property':
                            structures['property_decorators'].add(n.name)
                        elif decorator.id == 'staticmethod':
                            structures['static_methods'].add(n.name)
                        elif decorator.id == 'classmethod':
                            structures['class_methods'].add(n.name)
                        elif decorator.id == 'abstractmethod':
                            structures['abstract_methods'].add(n.name)
                    elif isinstance(decorator, ast.Call):
                        structures['decorators_with_args'][n.name] = extract_decorator(decorator)
            except Exception:
                decorators = []
            
            # Analyze function body
            for child in ast.walk(n):
                if isinstance(child, ast.Yield) or isinstance(child, ast.YieldFrom):
                    structures['yield_exprs'].append({
                        'func_name': n.name,
                        'expr': ast.unparse(child)
                    })
                elif isinstance(child, ast.Await):
                    structures['await_exprs'].append({
                        'func_name': n.name,
                        'expr': ast.unparse(child)
                    })
                elif isinstance(child, ast.Global):
                    structures['global_vars'].update(child.names)
                elif isinstance(child, ast.Nonlocal):
                    structures['nonlocal_vars'].update(child.names)
                elif isinstance(child, ast.AsyncWith):
                    structures['async_with'].append({
                        'func_name': n.name,
                        'items': [ast.unparse(item) for item in child.items],
                        'body': [ast.unparse(stmt) for stmt in child.body]
                    })
                elif isinstance(child, ast.AsyncFor):
                    structures['async_for'].append({
                        'func_name': n.name,
                        'target': ast.unparse(child.target),
                        'iter': ast.unparse(child.iter),
                        'body': [ast.unparse(stmt) for stmt in child.body]
                    })
            
            # Analyze nested functions
            nested_funcs = {}
            for child in ast.walk(n):
                if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)) and child is not n:
                    nested_funcs[child.name] = {
                        'is_async': isinstance(child, ast.AsyncFunctionDef),
                        'args': [a.arg for a in child.args.args],
                        'decorators': [extract_decorator(d) for d in child.decorator_list],
                        'docstring': ast.get_docstring(child),
                        'body': child.body,
                        'node': child,
                        'returns': ast.unparse(child.returns) if child.returns else None
                    }
            
            func_info = {
                'args': args,
                'returns': returns,
                'decorators': decorators,
                'is_async': is_async,
                'body': n.body,
                'docstring': ast.get_docstring(n),
                'nested_functions': nested_funcs,
                'node': n,
                'is_generator': any(isinstance(child, (ast.Yield, ast.YieldFrom)) for child in ast.walk(n)),
                'has_async_with': any(isinstance(child, ast.AsyncWith) for child in ast.walk(n)),
                'has_async_for': any(isinstance(child, ast.AsyncFor) for child in ast.walk(n))
            }
            
            if is_async:
                structures['async_functions'][n.name] = func_info
            else:
                structures['functions'][n.name] = func_info
            
            structures['decorators'].update(decorators)
    
    # Analyze classes
    for n in ast.walk(node):
        if isinstance(n, ast.ClassDef):
            methods = []
            async_methods = []
            class_vars = []
            decorators = [extract_decorator(d) for d in n.decorator_list]
            
            # Check for dataclass
            is_dataclass = any(d.id == 'dataclass' for d in n.decorator_list if isinstance(d, ast.Name))
            
            # Process class body
            for item in n.body:
                if isinstance(item, ast.FunctionDef):
                    method_info = {
                        'name': item.name,
                        'decorators': [extract_decorator(d) for d in item.decorator_list],
                        'is_property': any(d.id == 'property' for d in item.decorator_list if isinstance(d, ast.Name)),
                        'is_classmethod': any(d.id == 'classmethod' for d in item.decorator_list if isinstance(d, ast.Name)),
                        'is_staticmethod': any(d.id == 'staticmethod' for d in item.decorator_list if isinstance(d, ast.Name)),
                        'is_abstract': any(d.id == 'abstractmethod' for d in item.decorator_list if isinstance(d, ast.Name)),
                        'body': item.body,
                        'node': item,
                        'args': [a.arg for a in item.args.args],
                        'returns': ast.unparse(item.returns) if item.returns else None
                    }
                    methods.append(method_info)
                elif isinstance(item, ast.AsyncFunctionDef):
                    async_methods.append({
                        'name': item.name,
                        'decorators': [extract_decorator(d) for d in item.decorator_list],
                        'body': item.body,
                        'node': item,
                        'args': [a.arg for a in item.args.args],
                        'returns': ast.unparse(item.returns) if item.returns else None
                    })
                elif isinstance(item, ast.AnnAssign):
                    if isinstance(item.target, ast.Name):
                        annotation = ast.unparse(item.annotation)
                        value = ast.unparse(item.value) if item.value else None
                        is_classvar = (
                            isinstance(item.annotation, ast.Subscript) and 
                            isinstance(item.annotation.value, ast.Name) and 
                            item.annotation.value.id == 'ClassVar'
                        )
                        is_dataclass_field = (
                            is_dataclass and
                            isinstance(item.annotation, ast.Call) and
                            isinstance(item.annotation.func, ast.Name) and
                            item.annotation.func.id == 'field'
                        )
                        
                        class_vars.append({
                            'name': item.target.id,
                            'type': annotation,
                            'value': value,
                            'is_class_var': is_classvar,
                            'is_dataclass_field': is_dataclass_field
                        })
                        
                        if is_dataclass_field:
                            structures['dataclasses'][item.target.id] = {
                                'type': annotation,
                                'default': value,
                                'metadata': {
                                    k.arg: ast.unparse(k.value)
                                    for k in item.annotation.keywords
                                }
                            }
                elif isinstance(item, ast.ClassDef):
                    structures['nested_classes'][item.name] = analyze_complex_structures(item, source_code)
            
            # Process metaclass
            metaclass = None
            for keyword in n.keywords:
                if keyword.arg == 'metaclass':
                    metaclass = ast.unparse(keyword.value)
            
            # Process bases with generic types
            bases = []
            for base in n.bases:
                if isinstance(base, ast.Name):
                    bases.append(base.id)
                elif isinstance(base, ast.Subscript):  # Generic types like List[int]
                    bases.append(ast.unparse(base))
                else:
                    bases.append(ast.unparse(base))
            
            structures['classes'][n.name] = {
                'methods': methods,
                'async_methods': async_methods,
                'bases': bases,
                'decorators': decorators,
                'class_vars': class_vars,
                'docstring': ast.get_docstring(n),
                'metaclass': metaclass,
                'node': n,
                'is_dataclass': is_dataclass,
                'is_protocol': any(base == 'Protocol' for base in bases)
            }
            
            structures['decorators'].update(decorators)
    
    # Analyze comprehensions and generators
    for n in ast.walk(node):
        if isinstance(n, (ast.ListComp, ast.SetComp, ast.DictComp)):
            structures['comprehensions'].append({
                'type': type(n).__name__,
                'code': ast.unparse(n)
            })
        elif isinstance(n, ast.GeneratorExp):
            structures['generators'].append({
                'code': ast.unparse(n)
            })
        elif isinstance(n, ast.Lambda):
            structures['lambda_funcs'].append({
                'args': [ast.unparse(arg) for arg in n.args.args],
                'body': ast.unparse(n.body)
            })
    
    # Analyze match statements (Python 3.10+)
    for n in ast.walk(node):
        if hasattr(ast, 'Match') and isinstance(n, ast.Match):
            structures['match_cases'].append({
                'subject': ast.unparse(n.subject),
                'cases': [{
                    'pattern': ast.unparse(case.pattern),
                    'guard': ast.unparse(case.guard) if case.guard else None,
                    'body': [ast.unparse(stmt) for stmt in case.body]
                } for case in n.cases]
            })
    
    # Analyze context managers (with blocks)
    for n in ast.walk(node):
        if isinstance(n, ast.With):
            structures['with_blocks'].append({
                'items': [ast.unparse(item) for item in n.items],
                'body': [ast.unparse(stmt) for stmt in n.body]
            })
        elif isinstance(n, ast.AsyncWith):
            structures['async_with'].append({
                'items': [ast.unparse(item) for item in n.items],
                'body': [ast.unparse(stmt) for stmt in n.body]
            })
    
    # Analyze try-except blocks
    for n in ast.walk(node):
        if isinstance(n, ast.Try):
            structures['try_blocks'].append({
                'body': [ast.unparse(stmt) for stmt in n.body],
                'handlers': [{
                    'type': ast.unparse(handler.type) if handler.type else None,
                    'name': handler.name,
                    'body': [ast.unparse(stmt) for stmt in handler.body]
                } for handler in n.handlers],
                'finally_body': [ast.unparse(stmt) for stmt in n.finalbody] if n.finalbody else None,
                'else_body': [ast.unparse(stmt) for stmt in n.orelse] if n.orelse else None
            })
    
    # Analyze f-strings
    for n in ast.walk(node):
        if isinstance(n, ast.JoinedStr):
            structures['f_strings'].append({
                'code': ast.unparse(n)
            })
    
    # Analyze type comments
    for n in ast.walk(node):
        if hasattr(n, 'type_comment') and n.type_comment:
            structures['type_comments'][ast.unparse(n)] = n.type_comment
    
    return structures

def get_parent_class(node: ast.ClassDef, tree: ast.AST) -> Optional[ast.ClassDef]:
    """Get the parent class node for a given class node."""
    for parent in ast.walk(tree):
        if isinstance(parent, ast.ClassDef):
            for child in ast.walk(parent):
                if child == node and child is not parent:
                    return parent
    return None

def is_node_in_function_or_class(node: ast.AST, tree: ast.AST) -> bool:
    """Check if a node is inside a function or class definition."""
    return get_parent_function_or_class(node, tree) is not None 