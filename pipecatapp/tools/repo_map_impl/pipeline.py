from __future__ import annotations

from pathlib import Path

from pipecatapp.tools.repo_map_impl.cache import TagCache
from pipecatapp.tools.repo_map_impl.config import RepoMapConfig, load_config
from pipecatapp.tools.repo_map_impl.discover import discover_files
from pipecatapp.tools.repo_map_impl.extract.python_ast import enrich_python
from pipecatapp.tools.repo_map_impl.extract.tree_sitter import (
    extract_tags,
    file_symbols_from_cache,
    file_symbols_to_cache_payload,
)
from pipecatapp.tools.repo_map_impl.model import FileSymbols
from pipecatapp.tools.repo_map_impl.rank import format_file_brief, select_budget_map
from pipecatapp.tools.repo_map_impl.render.catalog import render_catalog_section
from pipecatapp.tools.repo_map_impl.render.file_index import render_file_index
from pipecatapp.tools.repo_map_impl.render.json_out import render_json
from pipecatapp.tools.repo_map_impl.render.navigation import (
    compact_tree_threshold,
    compute_section_lines,
    render_agent_guide,
)
from pipecatapp.tools.repo_map_impl.render.tree import render_aider_section


def _cache_dir(root: Path) -> Path:
    return root / ".repo-map-cache"


def extract_all(
    root: Path,
    file_paths: list[Path],
    *,
    use_cache: bool = True,
    enrich_python_files: bool = False,
) -> list[FileSymbols]:
    cache = TagCache(_cache_dir(root)) if use_cache else None
    results: list[FileSymbols] = []

    for path in file_paths:
        cached = None
        if cache:
            cached = cache.get(path)
        if cached:
            fs = file_symbols_from_cache(cached)
        else:
            fs = extract_tags(path, root)
            if cache and not fs.error:
                cache.set(path, file_symbols_to_cache_payload(fs))

        if enrich_python_files and fs.language == "python":
            fs = enrich_python(fs, path)

        results.append(fs)

    return results


def generate_full_map(
    root: Path,
    *,
    max_files: int | None = None,
    enrich_python_files: bool = False,
    config: RepoMapConfig | None = None,
    tree_detail: bool = False,
) -> str:
    root = root.resolve()
    config = config or load_config(root)
    paths = discover_files(root, max_files=max_files, extra_exclude_globs=config.exclude_globs)
    files = extract_all(root, paths, enrich_python_files=enrich_python_files)

    threshold = compact_tree_threshold(config)
    use_compact_tree = len(files) > threshold and not tree_detail

    file_index = render_file_index(files, config)
    catalog = render_catalog_section(
        files,
        config,
        include_file_index=True,
        file_index_text=file_index,
    )
    tree = render_aider_section(root.name, files, compact=use_compact_tree)

    # Catalog before tree: agents grep symbol detail first; tree is layout appendix.
    body = "\n\n".join([catalog, tree])
    total_lines = body.count("\n") + 1

    section_lines = compute_section_lines(
        body,
        {
            "Code intelligence catalog": "<!-- repo-map:section=catalog -->",
            "Directory tree": "<!-- repo-map:section=tree -->",
        },
    )

    guide_stub = render_agent_guide(
        root.name,
        files,
        section_lines={},
        compact_tree=use_compact_tree,
        total_lines=total_lines,
    )
    # First line of `body` in the full document (1-based).
    body_start_line = len(guide_stub.splitlines()) + 2
    adjusted = {
        name: (start + body_start_line - 1, end + body_start_line - 1)
        for name, (start, end) in section_lines.items()
    }
    full_line_count = body_start_line - 1 + total_lines
    guide = render_agent_guide(
        root.name,
        files,
        section_lines=adjusted,
        compact_tree=use_compact_tree,
        total_lines=full_line_count,
    )

    return guide + "\n\n" + body


def generate_budget_map(
    root: Path,
    budget: int,
    *,
    focus_files: list[str] | None = None,
    max_files: int | None = None,
    enrich_python_files: bool = False,
    config: RepoMapConfig | None = None,
) -> str:
    root = root.resolve()
    config = config or load_config(root)
    paths = discover_files(root, max_files=max_files, extra_exclude_globs=config.exclude_globs)
    files = extract_all(root, paths, enrich_python_files=enrich_python_files)

    header = (
        "<!-- repo-map-format: 1 (focused) -->\n"
        "<!-- AGENTS: This is a ranked subset. Use grep on .repo-map.md --full for exhaustive index. -->\n\n"
    )
    return header + select_budget_map(
        files,
        budget,
        focus_files=focus_files,
        format_file=format_file_brief,
    )
