from __future__ import annotations

from collections import defaultdict
from pathlib import Path

from pipecatapp.tools.repo_map_impl.config import RepoMapConfig
from pipecatapp.tools.repo_map_impl.model import FileSymbols
from pipecatapp.tools.repo_map_impl.render.catalog import categorize_files

# Above this file count, full maps use a paths-only tree unless --tree-detail.
DEFAULT_COMPACT_TREE_THRESHOLD = 100


def compact_tree_threshold(config: RepoMapConfig | None) -> int:
    if config and config.compact_tree_threshold is not None:
        return config.compact_tree_threshold
    return DEFAULT_COMPACT_TREE_THRESHOLD


def render_agent_guide(
    repo_name: str,
    files: list[FileSymbols],
    *,
    section_lines: dict[str, tuple[int, int]],
    compact_tree: bool,
    total_lines: int,
) -> str:
    """Preamble agents must read before scanning the rest of the map."""
    file_count = len(files)
    large = file_count > compact_tree_threshold(None) or total_lines > 4000

    lines = [
        "<!-- repo-map-format: 1 -->",
        "<!-- AGENTS: Read 'How agents should use this map' below. Do NOT load the entire file. -->",
        "",
        f"# Repository map: {repo_name}",
        "",
        "## How agents should use this map",
        "",
        "**Do not read this file end-to-end.** It is an index, not source code. Loading all "
        f"~{total_lines:,} lines will waste context and can overflow the window.",
        "",
        "### Safe navigation (required)",
        "",
        "1. **Read only this section first** (the guide + quick index).",
        "2. **Locate targets** with search tools — do not scroll the whole map:",
        "   - `grep -n \"### \\`path/to/file\" .repo-map.md` — jump to a file entry in the catalog",
        "   - `grep -n \"## Services\" .repo-map.md` — jump to a category",
        "   - `grep -n \"class YourClass\" .repo-map.md` — find a symbol name",
        "3. **Read a small line range** around matches (`read_file` with offset/limit, or `sed -n '1200,1250p'`).",
        "4. **Open real source** under the repo for implementation detail — the map is not a substitute.",
        "",
        "### Which section to use",
        "",
        "| Section | When to use |",
        "|---------|-------------|",
        "| **Quick index** (below) | Pick a category or directory before searching |",
        "| **Code intelligence catalog** | APIs, exports, classes, functions, docstrings |",
        f"| **Directory tree** | Path layout only{' (compact: no per-file symbols)' if compact_tree else ''} |",
        "",
        "### If this map is too large",
        "",
    ]

    if large:
        lines.extend(
            [
                f"This map indexes **{file_count}** source files. Prefer a focused map instead of reading `--full`:",
                "",
                "```bash",
                f"repo-map \"$PROJECT_ROOT\" --budget 8000",
                f"repo-map \"$PROJECT_ROOT\" --budget 8000 --focus path/under/edit",
                "```",
                "",
                "Use `--full` output only via **grep + partial reads**, or regenerate with `--budget`.",
                "",
            ]
        )
    else:
        lines.append(
            "Use grep + partial reads on this file, or `--budget` if you only need the most relevant symbols."
        )
        lines.append("")

    lines.extend(["## Quick index", ""])

    if section_lines:
        lines.append("| Section | Start line | End line |")
        lines.append("|---------|------------|----------|")
        for name, (start, end) in section_lines.items():
            lines.append(f"| {name} | {start} | {end} |")
        lines.append("")

    categories = categorize_files(files)
    lines.append("### Categories (file counts)")
    for cat, cat_files in sorted(categories.items(), key=lambda x: (-len(x[1]), x[0])):
        if not cat_files:
            continue
        title = cat.replace("_", " ").title()
        samples = ", ".join(f"`{f.path}`" for f in sorted(cat_files, key=lambda f: f.path)[:4])
        more = len(cat_files) - 4
        suffix = f" (+{more} more — grep catalog)" if more > 0 else ""
        lines.append(f"- **{title}** ({len(cat_files)}): {samples}{suffix}")
    lines.append("")

    dir_counts: dict[str, int] = defaultdict(int)
    for fs in files:
        parts = Path(fs.path).parts
        top = parts[0] if parts else "."
        dir_counts[top] += 1

    lines.append("### Top-level directories")
    for name, count in sorted(dir_counts.items(), key=lambda x: (-x[1], x[0])):
        lines.append(f"- `{name}/` — {count} files")
    lines.append("")

    lines.append("---")
    lines.append("")
    return "\n".join(lines)


def compute_section_lines(full_text: str, markers: dict[str, str]) -> dict[str, tuple[int, int]]:
    """Return 1-based inclusive line ranges for each marker comment in the document."""
    line_list = full_text.splitlines()
    positions: dict[str, int] = {}
    for i, line in enumerate(line_list, start=1):
        for key, token in markers.items():
            if token in line:
                positions[key] = i

    ranges: dict[str, tuple[int, int]] = {}
    ordered = sorted(positions.items(), key=lambda x: x[1])
    for idx, (key, start) in enumerate(ordered):
        end = (ordered[idx + 1][1] - 1) if idx + 1 < len(ordered) else len(line_list)
        ranges[key] = (start, end)
    return ranges
