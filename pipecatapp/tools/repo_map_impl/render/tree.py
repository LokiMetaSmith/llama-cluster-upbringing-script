from __future__ import annotations

from pathlib import Path

from pipecatapp.tools.repo_map_impl.model import FileSymbols


def build_tree(files: list[FileSymbols]) -> dict:
    tree: dict = {}
    for fs in files:
        parts = Path(fs.path).parts
        current = tree
        for part in parts[:-1]:
            current = current.setdefault(part, {})
        leaf = {
            "classes": fs.tree_classes(),
            "functions": fs.tree_functions(),
        }
        if fs.error:
            leaf["error"] = fs.error
        current[parts[-1]] = leaf
    return tree


def format_tree_compact(tree: dict, prefix: str = "") -> str:
    """Paths only — no per-file symbols (for large repos)."""
    lines: list[str] = []
    items = sorted(tree.items())
    for i, (name, content) in enumerate(items):
        is_last = i == len(items) - 1
        current_prefix = "└── " if is_last else "├── "
        if isinstance(content, dict) and (
            "classes" in content or "functions" in content or "error" in content
        ):
            lines.append(f"{prefix}{current_prefix}{name}")
        else:
            lines.append(f"{prefix}{current_prefix}{name}/")
            next_prefix = prefix + ("    " if is_last else "│   ")
            lines.append(format_tree_compact(content, next_prefix))
    return "\n".join(lines)


def format_tree(tree: dict, prefix: str = "") -> str:
    lines: list[str] = []
    items = sorted(tree.items())
    for i, (name, content) in enumerate(items):
        is_last = i == len(items) - 1
        current_prefix = "└── " if is_last else "├── "
        if isinstance(content, dict) and ("classes" in content or "functions" in content or "error" in content):
            lines.append(f"{prefix}{current_prefix}{name}")
            branch = "    " if is_last else "│   "
            for cls in content.get("classes") or []:
                lines.append(f"{prefix}{branch}    class {cls}")
            for func in content.get("functions") or []:
                lines.append(f"{prefix}{branch}    def {func}()")
            if content.get("error"):
                lines.append(f"{prefix}{branch}    # Error: {content['error']}")
        else:
            lines.append(f"{prefix}{current_prefix}{name}/")
            next_prefix = prefix + ("    " if is_last else "│   ")
            lines.append(format_tree(content, next_prefix))
    return "\n".join(lines)


def render_aider_section(
    repo_name: str,
    files: list[FileSymbols],
    *,
    compact: bool = False,
) -> str:
    tree = build_tree(files)
    tree_body = format_tree_compact(tree) if compact else format_tree(tree)
    mode = "compact paths only" if compact else "with symbols"
    out = [
        "<!-- repo-map:section=tree -->",
        "=" * 80,
        f"REPOSITORY MAP (Aider Style — {mode})",
        "=" * 80,
        f"Repository: {repo_name}",
        "",
        f"Total source files: {len(files)}",
        "",
    ]
    if compact:
        out.append(
            "_Symbol detail is in the Code Intelligence Catalog above. "
            "Use grep on that section for classes/functions._"
        )
        out.append("")
    out.extend([tree_body, "", "=" * 80])
    return "\n".join(out)
