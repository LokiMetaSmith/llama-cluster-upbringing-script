from __future__ import annotations

from pipecatapp.tools.repo_map_impl.config import RepoMapConfig
from pipecatapp.tools.repo_map_impl.model import FileSymbols
from pipecatapp.tools.repo_map_impl.render.catalog import categorize_files


def render_file_index(files: list[FileSymbols], config: RepoMapConfig | None = None) -> str:
    """One path per line per category — cheap to grep, no symbol detail."""
    categories = categorize_files(files, config)
    lines = [
        "## File path index",
        "",
        "Use `grep` on paths below, then open the matching `### \\`path\\`` section in this catalog.",
        "",
    ]

    for category, cat_files in categories.items():
        if not cat_files:
            continue
        title = category.replace("_", " ").title()
        lines.append(f"### {title} ({len(cat_files)} files)")
        for fs in sorted(cat_files, key=lambda f: f.path):
            lines.append(f"- `{fs.path}`")
        lines.append("")

    return "\n".join(lines)
