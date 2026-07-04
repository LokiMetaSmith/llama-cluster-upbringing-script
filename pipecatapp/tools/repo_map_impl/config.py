from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml


@dataclass
class RepoMapConfig:
    exclude_globs: list[str] = field(default_factory=list)
    categories: dict[str, list[str]] = field(default_factory=dict)
    compact_tree_threshold: int | None = None


def load_config(root: Path) -> RepoMapConfig:
    for name in ("repo-map.yaml", "repo-map.yml"):
        path = root / name
        if not path.is_file():
            continue
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        except (OSError, yaml.YAMLError):
            return RepoMapConfig()
        threshold = data.get("compact_tree_threshold")
        return RepoMapConfig(
            exclude_globs=list(data.get("exclude_globs") or []),
            categories=dict(data.get("categories") or {}),
            compact_tree_threshold=int(threshold) if threshold is not None else None,
        )
    return RepoMapConfig()
