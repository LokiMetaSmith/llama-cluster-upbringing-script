from __future__ import annotations

from collections import defaultdict

from pipecatapp.tools.repo_map_impl.model import FileSymbols


def estimate_tokens(text: str) -> int:
    return max(1, len(text) // 4)


def build_reference_graph(files: list[FileSymbols]) -> dict[str, set[str]]:
    """file_path -> set of file_paths it references (by symbol name heuristics)."""
    defs_by_name: dict[str, set[str]] = defaultdict(set)
    for fs in files:
        for s in fs.symbols:
            if s.role == "definition":
                defs_by_name[s.name].add(fs.path)
        for name in fs.exports:
            defs_by_name[name].add(fs.path)

    graph: dict[str, set[str]] = defaultdict(set)
    for fs in files:
        for s in fs.symbols:
            if s.role != "reference":
                continue
            for target in defs_by_name.get(s.name, ()):
                if target != fs.path:
                    graph[fs.path].add(target)
    return graph


def pagerank(
    graph: dict[str, set[str]],
    *,
    nodes: list[str],
    personalization: dict[str, float] | None = None,
    iterations: int = 20,
    damping: float = 0.85,
) -> dict[str, float]:
    if not nodes:
        return {}
    scores = {n: 1.0 / len(nodes) for n in nodes}
    out_weight = {n: max(len(graph.get(n, ())), 1) for n in nodes}

    pers = personalization
    if pers:
        total = sum(pers.values()) or 1.0
        pers = {k: v / total for k, v in pers.items()}

    for _ in range(iterations):
        new_scores: dict[str, float] = {}
        for n in nodes:
            rank = (1 - damping) / len(nodes)
            if pers and n in pers:
                rank = (1 - damping) * pers.get(n, 0)
            incoming = 0.0
            for src in nodes:
                if n in graph.get(src, ()):
                    incoming += scores[src] / out_weight[src]
            new_scores[n] = rank + damping * incoming
        scores = new_scores
    return scores


def select_budget_map(
    files: list[FileSymbols],
    budget: int,
    *,
    focus_files: list[str] | None = None,
    format_file,
) -> str:
    """Return markdown fitting within approximate token budget."""
    nodes = [f.path for f in files]
    graph = build_reference_graph(files)
    pers = None
    if focus_files:
        pers = {p: 2.0 for p in focus_files if p in nodes}
    ranks = pagerank(graph, nodes=nodes, personalization=pers)
    if not ranks:
        ranks = {f.path: 1.0 for f in files}

    by_path = {f.path: f for f in files}
    ordered = sorted(files, key=lambda f: (-ranks.get(f.path, 0), f.path))

    parts: list[str] = []
    used = 0
    header = "# Repository Map (focused)\n\n"
    parts.append(header)
    used += estimate_tokens(header)

    for fs in ordered:
        chunk = format_file(fs)
        cost = estimate_tokens(chunk)
        if used + cost > budget and parts:
            break
        parts.append(chunk)
        used += cost

    return "\n".join(parts)


def format_file_brief(fs: FileSymbols) -> str:
    lines = [f"## `{fs.path}` ({fs.language})"]
    defs = [s for s in fs.symbols if s.role == "definition"]
    if fs.classes:
        for cls in fs.classes:
            methods = ", ".join(m.name for m in cls.methods if m.is_public)[:80]
            lines.append(f"- class `{cls.name}`" + (f" — {methods}" if methods else ""))
    elif defs:
        for s in defs[:12]:
            lines.append(f"- {s.kind} `{s.name}` (L{s.line})")
    if fs.exports:
        lines.append(f"- exports: {', '.join(fs.exports[:8])}")
    lines.append("")
    return "\n".join(lines)
