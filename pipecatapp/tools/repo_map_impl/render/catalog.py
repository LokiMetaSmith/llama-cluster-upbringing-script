from __future__ import annotations

from pipecatapp.tools.repo_map_impl.config import RepoMapConfig
from pipecatapp.tools.repo_map_impl.model import FileSymbols


def default_categorize(path: str) -> str:
    lower = path.lower()
    if "__main__" in path or "main.py" in path or "run.py" in path:
        return "entry_points"
    if "service" in lower:
        return "services"
    if "model" in lower:
        return "models"
    if "config" in lower or "settings" in lower:
        return "configuration"
    if "util" in lower or "helper" in lower:
        return "utilities"
    return "other"


def categorize_files(
    files: list[FileSymbols], config: RepoMapConfig | None = None
) -> dict[str, list[FileSymbols]]:
    categories: dict[str, list[FileSymbols]] = {
        "entry_points": [],
        "services": [],
        "models": [],
        "utilities": [],
        "configuration": [],
        "other": [],
    }
    custom = (config.categories if config else {}) or {}

    for fs in files:
        assigned = None
        for cat, patterns in custom.items():
            for pat in patterns:
                if pat in fs.path:
                    assigned = cat
                    break
            if assigned:
                break
        if not assigned:
            assigned = default_categorize(fs.path)
        categories.setdefault(assigned, []).append(fs)

    return categories


def render_catalog_section(
    files: list[FileSymbols],
    config: RepoMapConfig | None = None,
    *,
    include_file_index: bool = True,
    file_index_text: str = "",
) -> str:
    categories = categorize_files(files, config)
    lines = [
        "<!-- repo-map:section=catalog -->",
        "# Repository Code Intelligence Map (Sourcegraph Style)",
        "",
    ]
    if include_file_index and file_index_text:
        lines.append(file_index_text)
        lines.append("---")
        lines.append("")
    lines.append("## Overview")
    lines.append("")
    lines.append(f"Total files analyzed: {len(files)}")
    lines.append("")

    for category, cat_files in categories.items():
        if not cat_files:
            continue
        title = category.replace("_", " ").title()
        lines.append(f"## {title}")
        lines.append("")
        for fs in sorted(cat_files, key=lambda f: f.path):
            lines.append(f"### `{fs.path}`")
            if fs.docstring:
                lines.append(f"> {fs.docstring[:100]}...")
            lines.append("")
            if fs.exports:
                lines.append(f"**Exports:** {', '.join(fs.exports[:8])}")
                lines.append("")
            if fs.classes:
                lines.append("**Classes:**")
                for cls in fs.classes:
                    pub = [m.name for m in cls.methods if m.is_public]
                    if cls.bases:
                        lines.append(f"- `{cls.name}` (inherits: {', '.join(cls.bases)})")
                    else:
                        lines.append(f"- `{cls.name}`")
                    if pub:
                        lines.append(f"  - Methods: {', '.join(pub[:5])}")
                lines.append("")
            elif fs.symbols:
                defs = [s for s in fs.symbols if s.role == "definition"][:15]
                if defs:
                    lines.append("**Definitions:**")
                    for s in defs:
                        lines.append(f"- `{s.name}` ({s.kind}, L{s.line})")
                    lines.append("")
            if fs.functions:
                pub = [f for f in fs.functions if f.is_public][:5]
                if pub:
                    lines.append("**Functions:**")
                    for fn in pub:
                        params = ", ".join(fn.params[:3])
                        lines.append(f"- `{fn.name}({params})`")
                    lines.append("")
            if fs.error:
                lines.append(f"⚠️ _Error parsing file: {fs.error}_")
                lines.append("")

    return "\n".join(lines)
