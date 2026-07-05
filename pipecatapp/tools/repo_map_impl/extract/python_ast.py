from __future__ import annotations

import ast
from pathlib import Path

from pipecatapp.tools.repo_map_impl.model import ClassInfo, FileSymbols, FunctionInfo, ImportInfo, MethodInfo


def _get_name(node: ast.expr) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return f"{_get_name(node.value)}.{node.attr}"
    return str(node)


def enrich_python(fs: FileSymbols, file_path: Path) -> FileSymbols:
    if fs.language != "python" or fs.error:
        return fs
    try:
        content = file_path.read_text(encoding="utf-8")
        tree = ast.parse(content, filename=str(file_path))
    except Exception as e:
        fs.error = str(e)
        return fs

    fs.docstring = ast.get_docstring(tree) or ""
    fs.classes = []
    fs.functions = []
    fs.imports = []
    fs.exports = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                fs.imports.append(ImportInfo(module=alias.name, alias=alias.asname))
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            for alias in node.names:
                fs.imports.append(
                    ImportInfo(from_module=module, name=alias.name, alias=alias.asname)
                )

    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            methods = []
            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    methods.append(
                        MethodInfo(
                            name=item.name,
                            params=[a.arg for a in item.args.args],
                            is_public=not item.name.startswith("_"),
                        )
                    )
            cls = ClassInfo(
                name=node.name,
                methods=methods,
                bases=[_get_name(b) for b in node.bases],
                docstring=ast.get_docstring(node) or "",
                is_public=not node.name.startswith("_"),
            )
            fs.classes.append(cls)
            if cls.is_public:
                fs.exports.append(node.name)
        elif isinstance(node, ast.FunctionDef):
            fn = FunctionInfo(
                name=node.name,
                params=[a.arg for a in node.args.args],
                docstring=ast.get_docstring(node) or "",
                is_public=not node.name.startswith("_"),
            )
            fs.functions.append(fn)
            if fn.is_public:
                fs.exports.append(node.name)

    return fs
