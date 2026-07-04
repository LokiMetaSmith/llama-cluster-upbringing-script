from __future__ import annotations

import importlib
from pathlib import Path
from typing import Callable

from tree_sitter import Language, Parser, Query, QueryCursor

from pipecatapp.tools.repo_map_impl.languages import lang_for_path
from pipecatapp.tools.repo_map_impl.model import FileSymbols, Symbol

QUERIES_DIR = Path(__file__).resolve().parent.parent / "queries"

# lang_id -> (module_name, language_factory_attr)
GRAMMAR_SPECS: dict[str, tuple[str, str]] = {
    "python": ("tree_sitter_python", "language"),
    "go": ("tree_sitter_go", "language"),
    "rust": ("tree_sitter_rust", "language"),
    "javascript": ("tree_sitter_javascript", "language"),
    "typescript": ("tree_sitter_typescript", "language_typescript"),
    "tsx": ("tree_sitter_typescript", "language_tsx"),
    "swift": ("tree_sitter_swift", "language"),
}

_parser_cache: dict[str, Parser] = {}
_language_cache: dict[str, Language] = {}


def _load_language(lang: str) -> Language | None:
    if lang in _language_cache:
        return _language_cache[lang]
    spec = GRAMMAR_SPECS.get(lang)
    if not spec:
        return None
    mod_name, attr = spec
    try:
        mod = importlib.import_module(mod_name)
        factory: Callable = getattr(mod, attr)
        language = Language(factory())
        _language_cache[lang] = language
        return language
    except Exception:
        return None


def _get_parser(lang: str) -> Parser | None:
    if lang in _parser_cache:
        return _parser_cache[lang]
    language = _load_language(lang)
    if not language:
        return None
    parser = Parser(language)
    _parser_cache[lang] = parser
    return parser


def _query_path(lang: str) -> Path | None:
    path = QUERIES_DIR / f"{lang}-tags.scm"
    return path if path.is_file() and path.stat().st_size > 20 else None


def _kind_from_capture(capture: str) -> tuple[str, str]:
    if capture.startswith("name."):
        capture = capture[5:]
    if ".definition." in capture or capture.startswith("definition."):
        role = "definition"
        if "definition." in capture:
            kind = capture.split("definition.", 1)[-1].split(".")[0]
        else:
            kind = capture.split(".")[-1]
        return role, kind
    if ".reference." in capture or capture.startswith("reference."):
        return "reference", capture.split(".")[-1]
    if "definition" in capture:
        return "definition", capture.split(".")[-1]
    if "reference" in capture:
        return "reference", capture.split(".")[-1]
    return "definition", "symbol"


def extract_tags(file_path: Path, repo_root: Path) -> FileSymbols:
    lang = lang_for_path(file_path)
    rel = str(file_path.relative_to(repo_root))
    if not lang:
        return FileSymbols(path=rel, language="unknown")

    query_path = _query_path(lang)
    if not query_path:
        return FileSymbols(path=rel, language=lang, error=f"no tags query for {lang}")

    parser = _get_parser(lang)
    language = _load_language(lang)
    if not parser or not language:
        return FileSymbols(path=rel, language=lang, error=f"grammar not installed for {lang}")

    try:
        code = file_path.read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        return FileSymbols(path=rel, language=lang, error=str(e))

    try:
        query = Query(language, query_path.read_text(encoding="utf-8"))
        tree = parser.parse(code.encode("utf-8"))
        root = tree.root_node
        captures = QueryCursor(query).captures(root)
    except Exception as e:
        return FileSymbols(path=rel, language=lang, error=str(e))

    symbols: list[Symbol] = []
    for capture_name, nodes in captures.items():
        if "name" not in capture_name:
            continue
        role, kind = _kind_from_capture(capture_name)
        for node in nodes:
            name = code.encode("utf-8")[node.start_byte : node.end_byte].decode("utf-8", errors="replace")
            line = node.start_point[0] + 1
            symbols.append(Symbol(name=name, kind=kind, line=line, role=role))

    seen: set[tuple[str, int, str]] = set()
    unique: list[Symbol] = []
    for s in symbols:
        key = (s.name, s.line, s.role)
        if key in seen:
            continue
        seen.add(key)
        unique.append(s)

    fs = FileSymbols(path=rel, language=lang, symbols=unique)
    fs.exports = sorted({s.name for s in unique if s.role == "definition" and not s.name.startswith("_")})
    return fs


def file_symbols_to_cache_payload(fs: FileSymbols) -> dict:
    return {
        "path": fs.path,
        "language": fs.language,
        "symbols": [
            {"name": s.name, "kind": s.kind, "line": s.line, "role": s.role} for s in fs.symbols
        ],
        "exports": fs.exports,
        "error": fs.error,
    }


def file_symbols_from_cache(payload: dict) -> FileSymbols:
    fs = FileSymbols(
        path=payload["path"],
        language=payload.get("language", "unknown"),
        exports=list(payload.get("exports") or []),
        error=payload.get("error"),
    )
    for s in payload.get("symbols") or []:
        fs.symbols.append(
            Symbol(
                name=s["name"],
                kind=s.get("kind", "symbol"),
                line=int(s.get("line", 0)),
                role=s.get("role", "definition"),
            )
        )
    return fs
