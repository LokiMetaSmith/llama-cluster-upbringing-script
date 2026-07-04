from __future__ import annotations

import json
from pathlib import Path


class TagCache:
    def __init__(self, cache_dir: Path):
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _key_path(self, file_path: Path) -> Path:
        safe = str(file_path).replace("/", "_").replace(":", "_")
        return self.cache_dir / f"{safe}.json"

    def get(self, file_path: Path) -> dict | None:
        path = self._key_path(file_path)
        if not path.is_file():
            return None
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return None
        try:
            mtime = file_path.stat().st_mtime
        except OSError:
            return None
        if data.get("mtime") != mtime:
            return None
        return data.get("payload")

    def set(self, file_path: Path, payload: dict) -> None:
        try:
            mtime = file_path.stat().st_mtime
        except OSError:
            return
        path = self._key_path(file_path)
        path.write_text(
            json.dumps({"mtime": mtime, "payload": payload}, ensure_ascii=False),
            encoding="utf-8",
        )
