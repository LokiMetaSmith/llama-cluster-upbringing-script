from __future__ import annotations

import json

from pipecatapp.tools.repo_map_impl.model import FileSymbols


def render_json(files: list[FileSymbols]) -> str:
    payload = []
    for fs in files:
        payload.append(
            {
                "path": fs.path,
                "language": fs.language,
                "exports": fs.exports,
                "symbols": [
                    {"name": s.name, "kind": s.kind, "line": s.line, "role": s.role}
                    for s in fs.symbols
                ],
                "error": fs.error,
            }
        )
    return json.dumps(payload, indent=2, ensure_ascii=False)
