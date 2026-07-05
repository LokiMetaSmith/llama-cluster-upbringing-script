from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Symbol:
    name: str
    kind: str
    line: int
    role: str = "definition"


@dataclass
class MethodInfo:
    name: str
    params: list[str] = field(default_factory=list)
    is_public: bool = True


@dataclass
class ClassInfo:
    name: str
    methods: list[MethodInfo] = field(default_factory=list)
    bases: list[str] = field(default_factory=list)
    docstring: str = ""
    is_public: bool = True


@dataclass
class FunctionInfo:
    name: str
    params: list[str] = field(default_factory=list)
    docstring: str = ""
    is_public: bool = True


@dataclass
class ImportInfo:
    module: str = ""
    name: str = ""
    from_module: str = ""
    alias: str | None = None


@dataclass
class FileSymbols:
    path: str
    language: str
    symbols: list[Symbol] = field(default_factory=list)
    classes: list[ClassInfo] = field(default_factory=list)
    functions: list[FunctionInfo] = field(default_factory=list)
    exports: list[str] = field(default_factory=list)
    imports: list[ImportInfo] = field(default_factory=list)
    docstring: str = ""
    error: str | None = None

    def tree_classes(self) -> list[str]:
        if self.classes:
            out = []
            for cls in self.classes:
                pub = [m.name for m in cls.methods if m.is_public][:3]
                if pub:
                    more = len([m for m in cls.methods if m.is_public]) > 3
                    out.append(f"{cls.name} ({', '.join(pub)}{'...' if more else ''})")
                else:
                    out.append(cls.name)
            return out
        return [s.name for s in self.symbols if s.role == "definition" and "class" in s.kind]

    def tree_functions(self) -> list[str]:
        if self.functions:
            return [f.name for f in self.functions if f.is_public]
        funcs = []
        for s in self.symbols:
            if s.role != "definition":
                continue
            kind = s.kind
            if kind in ("call", "reference"):
                continue
            if "function" in kind or "method" in kind:
                if "class" not in kind:
                    funcs.append(s.name)
        return funcs
