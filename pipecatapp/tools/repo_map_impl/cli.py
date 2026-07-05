from __future__ import annotations

import argparse
import sys
from pathlib import Path

from pipecatapp.tools.repo_map_impl import __version__
from pipecatapp.tools.repo_map_impl.config import load_config
from pipecatapp.tools.repo_map_impl.pipeline import generate_budget_map, generate_full_map
from pipecatapp.tools.repo_map_impl.render.json_out import render_json
from pipecatapp.tools.repo_map_impl.discover import discover_files
from pipecatapp.tools.repo_map_impl.pipeline import extract_all


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="repo-map",
        description="Generate fast deterministic repository maps for AI agents (L0 comprehension).",
    )
    parser.add_argument(
        "target",
        nargs="?",
        default=".",
        help="Repository root to analyze (default: current directory)",
    )
    parser.add_argument(
        "--full",
        action="store_true",
        help="Generate full map (tree + catalog sections)",
    )
    parser.add_argument(
        "--budget",
        type=int,
        metavar="N",
        help="Generate token-budget-focused map (approximate tokens)",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        help="Output file path (default: <target>/.repo-map.md for --full)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit JSON symbol index instead of markdown",
    )
    parser.add_argument(
        "--enrich-python",
        action="store_true",
        help="Use Python AST for richer imports/docstrings on .py files",
    )
    parser.add_argument(
        "--max-files",
        type=int,
        default=None,
        help="Cap number of source files processed",
    )
    parser.add_argument(
        "--no-cache",
        action="store_true",
        help="Disable .repo-map-cache tag cache",
    )
    parser.add_argument(
        "--focus",
        action="append",
        default=[],
        metavar="PATH",
        help="Boost ranking for file paths (repeatable, used with --budget)",
    )
    parser.add_argument(
        "--tree-detail",
        action="store_true",
        help="Include per-file symbols in the tree section even for large repos",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    args = parser.parse_args(argv)
    target = Path(args.target).resolve()

    if not target.is_dir():
        print(f"Error: not a directory: {target}", file=sys.stderr)
        return 1

    if not args.full and args.budget is None and not args.json:
        args.full = True

    config = load_config(target)

    if args.json:
        paths = discover_files(
            target, max_files=args.max_files, extra_exclude_globs=config.exclude_globs
        )
        files = extract_all(
            target,
            paths,
            use_cache=not args.no_cache,
            enrich_python_files=args.enrich_python,
        )
        content = render_json(files)
    elif args.budget is not None:
        content = generate_budget_map(
            target,
            args.budget,
            focus_files=args.focus or None,
            max_files=args.max_files,
            enrich_python_files=args.enrich_python,
        )
    else:
        content = generate_full_map(
            target,
            max_files=args.max_files,
            enrich_python_files=args.enrich_python,
            config=config,
            tree_detail=args.tree_detail,
        )

    if args.output:
        out_path = Path(args.output)
        if not out_path.is_absolute():
            out_path = target / out_path
    elif args.budget is not None and not args.json:
        out_path = None
    elif args.json:
        out_path = target / ".repo-map.json"
    else:
        out_path = target / ".repo-map.md"

    if out_path is None:
        sys.stdout.write(content)
        if not content.endswith("\n"):
            sys.stdout.write("\n")
    else:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(content, encoding="utf-8")
        print(f"Wrote {out_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
