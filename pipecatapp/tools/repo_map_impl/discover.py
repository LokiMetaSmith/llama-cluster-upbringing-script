from __future__ import annotations

import subprocess
from pathlib import Path

import pathspec

from pipecatapp.tools.repo_map_impl.languages import SOURCE_GLOBS, lang_for_path, supported_extensions

DEFAULT_DIR_EXCLUDES = {
    ".git", ".hg", ".svn", "node_modules", "vendor", "dist", "build", "out",
    "target", ".venv", "venv", "__pycache__", ".pytest_cache", ".mypy_cache",
    ".repo-map-cache", ".tox", "eggs", ".eggs",
}


def _load_gitignore_spec(root: Path) -> pathspec.PathSpec | None:
    gi = root / ".gitignore"
    if not gi.is_file():
        return None
    try:
        lines = gi.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return None
    return pathspec.PathSpec.from_lines("gitwildmatch", lines)


def _is_ignored(rel: str, spec: pathspec.PathSpec | None) -> bool:
    parts = Path(rel).parts
    if parts and parts[0] in DEFAULT_DIR_EXCLUDES:
        return True
    for part in parts:
        if part in DEFAULT_DIR_EXCLUDES:
            return True
    if spec and spec.match_file(rel):
        return True
    return False


def discover_files(
    root: Path,
    *,
    max_files: int | None = None,
    extra_exclude_globs: list[str] | None = None,
) -> list[Path]:
    root = root.resolve()
    spec = _load_gitignore_spec(root)
    if extra_exclude_globs:
        extra = pathspec.PathSpec.from_lines("gitwildmatch", extra_exclude_globs)
        combined = list(spec.patterns if spec else []) + list(extra.patterns)
        spec = pathspec.PathSpec.from_lines("gitwildmatch", combined)

    files: list[Path] = []
    exts = supported_extensions()

    if (root / ".git").is_dir():
        try:
            result = subprocess.run(
                ["git", "ls-files", "-z", "--", *SOURCE_GLOBS],
                cwd=root,
                capture_output=True,
                check=True,
            )
            for raw in result.stdout.split(b"\0"):
                if not raw:
                    continue
                rel = raw.decode("utf-8", errors="replace")
                if _is_ignored(rel, spec):
                    continue
                p = root / rel
                if p.is_file() and p.suffix.lower() in exts:
                    files.append(p)
        except (subprocess.CalledProcessError, FileNotFoundError):
            files = []

    if not files:
        for path in root.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in exts:
                continue
            try:
                rel = str(path.relative_to(root))
            except ValueError:
                continue
            if _is_ignored(rel, spec):
                continue
            if lang_for_path(path) is None:
                continue
            files.append(path)

    files.sort()
    if max_files is not None and len(files) > max_files:
        files = files[:max_files]
    return files
