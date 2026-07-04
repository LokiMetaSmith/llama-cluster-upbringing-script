from __future__ import annotations

from pathlib import Path

EXTENSION_TO_LANG: dict[str, str] = {
    ".py": "python",
    ".pyw": "python",
    ".go": "go",
    ".rs": "rust",
    ".js": "javascript",
    ".jsx": "javascript",
    ".mjs": "javascript",
    ".cjs": "javascript",
    ".ts": "typescript",
    ".tsx": "tsx",
    ".swift": "swift",
}

SOURCE_GLOBS = tuple(f"*{ext}" for ext in EXTENSION_TO_LANG)


def lang_for_path(path: Path) -> str | None:
    return EXTENSION_TO_LANG.get(path.suffix.lower())


def supported_extensions() -> frozenset[str]:
    return frozenset(EXTENSION_TO_LANG)
