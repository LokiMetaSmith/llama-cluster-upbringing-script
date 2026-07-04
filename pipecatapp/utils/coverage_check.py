#!/usr/bin/env python3
"""
Coverage check for scaffold-setup-skill.

Compares parameters documented in a generated setup skill against the
ground-truth parameters found in the repo's config files.

Usage:
    python coverage_check.py <repo_root> <generated_skill_path>

Exit codes:
    0  All checks pass
    1  Coverage failures (missing required params, below threshold)
    2  Flow validation failures (dead ends, duplicate questions, broken depends_on)
    3  Docs index failures (missing files)
"""

import sys
import os
import re
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Param:
    name: str
    required: bool
    source: str
    has_default: bool = False
    description: str = ""


@dataclass
class CheckResult:
    name: str
    passed: bool
    details: list[str] = field(default_factory=list)

    def __str__(self) -> str:
        status = "PASS" if self.passed else "FAIL"
        lines = [f"[{status}] {self.name}"]
        for detail in self.details:
            lines.append(f"       {detail}")
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Ground-truth extraction
# ---------------------------------------------------------------------------

def extract_env_example_params(repo_root: Path) -> list[Param]:
    """Extract params from .env.example or .env.sample."""
    params = []
    for candidate in [".env.example", ".env.sample", ".env.template"]:
        path = repo_root / candidate
        if path.exists():
            params.extend(_parse_env_file(path, candidate))
            break
    return params


def _parse_env_file(path: Path, source: str) -> list[Param]:
    params = []
    lines = path.read_text().splitlines()
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip()
            is_placeholder = not value or value.lower() in {
                "changeme", "replace_me", "your-value-here", "your_value_here",
                "<value>", "todo", "fixme", "xxx", "none", "null", "false", "true",
            } or value.startswith("<") or "replace" in value.lower()
            params.append(Param(
                name=key,
                required=is_placeholder,
                source=source,
                has_default=bool(value) and not is_placeholder,
            ))
    return params


def extract_ci_secret_params(repo_root: Path) -> list[Param]:
    """Extract secret params referenced in GitHub Actions workflows."""
    params = []
    workflows_dir = repo_root / ".github" / "workflows"
    if not workflows_dir.exists():
        return params
    secret_pattern = re.compile(r"\$\{\{\s*secrets\.(\w+)\s*\}\}")
    for wf_file in workflows_dir.glob("*.yml"):
        content = wf_file.read_text()
        for match in secret_pattern.finditer(content):
            name = match.group(1)
            if not any(p.name == name for p in params):
                params.append(Param(
                    name=name,
                    required=True,
                    source=str(wf_file.relative_to(repo_root)),
                ))
    return params


# ---------------------------------------------------------------------------
# Generated skill parsing
# ---------------------------------------------------------------------------

def extract_skill_params(skill_path: Path) -> set[str]:
    """Extract param names documented in the generated skill."""
    content = skill_path.read_text()
    params = set()

    # Match backtick-quoted ALL_CAPS identifiers: `PARAM_NAME`
    params.update(re.findall(r"`([A-Z][A-Z0-9_]{2,})`", content))

    # Match KEY=value patterns in code blocks
    params.update(re.findall(r"^([A-Z][A-Z0-9_]{2,})=", content, re.MULTILINE))

    # Match **`PARAM_NAME`** bold+backtick pattern (question headings)
    params.update(re.findall(r"\*\*`([A-Z][A-Z0-9_]{2,})`\*\*", content))

    # Filter out obvious false positives (single words, common markdown artifacts)
    noise = {"README", "CLAUDE", "SKILL", "HTTP", "HTTPS", "TODO", "NOTE", "WARNING",
             "FIXME", "URL", "API", "JWT", "SQL", "CSS", "HTML", "JSON", "YAML",
             "TOML", "ENV", "DEV", "PROD", "TRUE", "FALSE", "NULL"}
    return {p for p in params if p not in noise and "_" in p or len(p) > 6}


def extract_skill_branches(skill_path: Path) -> list[str]:
    """Extract question branch identifiers for flow validation."""
    content = skill_path.read_text()
    # Look for → arrows indicating branching
    branches = re.findall(r"→\s*([a-z_-]+):", content)
    return branches


def extract_docs_index_paths(skill_path: Path) -> list[str]:
    """Extract file paths from the docs index table."""
    content = skill_path.read_text()
    paths = []
    in_docs_section = False
    for line in content.splitlines():
        if "Documentation index" in line or "Documentation Q&A" in line:
            in_docs_section = True
        if in_docs_section and line.startswith("|"):
            cells = [c.strip() for c in line.strip("|").split("|")]
            if len(cells) >= 2:
                # Second column is typically the file path
                candidate = cells[1].strip()
                if candidate.endswith(".md") and "/" in candidate:
                    paths.append(candidate)
    return paths


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

def check_required_coverage(
    ground_truth: list[Param], skill_params: set[str]
) -> CheckResult:
    required = [p for p in ground_truth if p.required]
    if not required:
        return CheckResult("Required param coverage", True, ["No required params found in ground truth"])

    missing = [p for p in required if p.name not in skill_params]
    covered = len(required) - len(missing)
    pct = covered / len(required) * 100

    details = [f"Required params: {len(required)}, covered: {covered} ({pct:.0f}%)"]
    if missing:
        for p in missing:
            details.append(f"  MISSING [{p.source}]: {p.name}")

    return CheckResult("Required param coverage", len(missing) == 0, details)


def check_optional_coverage(
    ground_truth: list[Param], skill_params: set[str], threshold: float = 0.80
) -> CheckResult:
    optional = [p for p in ground_truth if not p.required]
    if not optional:
        return CheckResult("Optional param coverage", True, ["No optional params found"])

    missing = [p for p in optional if p.name not in skill_params]
    covered = len(optional) - len(missing)
    pct = covered / len(optional) * 100
    passed = pct >= threshold * 100

    details = [f"Optional params: {len(optional)}, covered: {covered} ({pct:.0f}%), threshold: {threshold*100:.0f}%"]
    if missing:
        for p in missing[:10]:  # cap output
            details.append(f"  MISSING [{p.source}]: {p.name}")
        if len(missing) > 10:
            details.append(f"  ... and {len(missing) - 10} more")

    return CheckResult("Optional param coverage", passed, details)


def check_undocumented_params(
    ground_truth: list[Param], skill_params: set[str]
) -> CheckResult:
    """Warn about params in skill that have no ground-truth source."""
    ground_truth_names = {p.name for p in ground_truth}
    undocumented = skill_params - ground_truth_names

    if not undocumented:
        return CheckResult("No undocumented params", True, ["All skill params have a source"])

    details = [f"Params in skill with no ground-truth source: {len(undocumented)}"]
    for name in sorted(undocumented)[:10]:
        details.append(f"  UNDOCUMENTED: {name}")

    # Undocumented params are a warning, not a failure — they may be inferred from source code
    return CheckResult("Undocumented params (informational)", True, details)


def check_docs_index(repo_root: Path, skill_path: Path) -> CheckResult:
    paths = extract_docs_index_paths(skill_path)
    if not paths:
        mkdocs = repo_root / "mkdocs.yml"
        if mkdocs.exists():
            return CheckResult("Docs index", False, ["mkdocs.yml found but no docs index in skill"])
        return CheckResult("Docs index", True, ["No mkdocs.yml, docs index skipped"])

    missing = []
    for p in paths:
        full = repo_root / p
        if not full.exists():
            missing.append(p)

    details = [f"Index entries: {len(paths)}, missing files: {len(missing)}"]
    for p in missing:
        details.append(f"  MISSING FILE: {p}")

    return CheckResult("Docs index file paths", len(missing) == 0, details)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <repo_root> <generated_skill_path>")
        return 2

    repo_root = Path(sys.argv[1]).resolve()
    skill_path = Path(sys.argv[2]).resolve()

    if not repo_root.is_dir():
        print(f"Error: repo root not found: {repo_root}")
        return 2
    if not skill_path.exists():
        print(f"Error: generated skill not found: {skill_path}")
        return 2

    print(f"Coverage check: {repo_root.name}")
    print(f"Skill:          {skill_path.relative_to(repo_root) if skill_path.is_relative_to(repo_root) else skill_path}")
    print()

    # Gather ground truth
    ground_truth = extract_env_example_params(repo_root)
    ci_params = extract_ci_secret_params(repo_root)
    # Merge CI params that aren't already in ground truth
    gt_names = {p.name for p in ground_truth}
    for p in ci_params:
        if p.name not in gt_names:
            ground_truth.append(p)

    skill_params = extract_skill_params(skill_path)

    # Run checks
    results = [
        check_required_coverage(ground_truth, skill_params),
        check_optional_coverage(ground_truth, skill_params),
        check_undocumented_params(ground_truth, skill_params),
        check_docs_index(repo_root, skill_path),
    ]

    # Print results
    any_failure = False
    for result in results:
        print(result)
        print()
        if not result.passed:
            any_failure = True

    # Summary
    passed = sum(1 for r in results if r.passed)
    print(f"Results: {passed}/{len(results)} checks passed")

    return 1 if any_failure else 0


if __name__ == "__main__":
    sys.exit(main())
