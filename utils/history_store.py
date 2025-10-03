"""Persistent storage for analysis history."""

from __future__ import annotations

import json
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List


class HistoryStore:
    """Append-only JSONL store that captures query analysis history."""

    def __init__(self, storage_path: Path) -> None:
        self.storage_path = storage_path
        self._lock = threading.Lock()
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.storage_path.exists():
            self.storage_path.write_text("", encoding="utf-8")

    def append(self, payload: Dict[str, Any]) -> None:
        """Persist a new analysis entry with a UTC timestamp."""
        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            **payload,
        }
        line = json.dumps(record, ensure_ascii=False)
        with self._lock:
            with self.storage_path.open("a", encoding="utf-8") as handle:
                handle.write(line + "\n")

    def get_recent(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Return the most recent history entries, newest last."""
        if limit <= 0 or not self.storage_path.exists():
            return []

        with self._lock:
            with self.storage_path.open("r", encoding="utf-8") as handle:
                lines = [line.strip() for line in handle if line.strip()]

        recent_lines = lines[-limit:]
        return [json.loads(line) for line in recent_lines]

    def metrics(self) -> Dict[str, Any]:
        """Return aggregate statistics about stored analyses."""
        if not self.storage_path.exists():
            return {
                "total_entries": 0,
                "first_run_at": None,
                "last_run_at": None,
            }

        with self._lock:
            with self.storage_path.open("r", encoding="utf-8") as handle:
                lines = [line.strip() for line in handle if line.strip()]

        if not lines:
            return {
                "total_entries": 0,
                "first_run_at": None,
                "last_run_at": None,
            }

        first_entry = json.loads(lines[0])
        last_entry = json.loads(lines[-1])

        return {
            "total_entries": len(lines),
            "first_run_at": first_entry.get("timestamp"),
            "last_run_at": last_entry.get("timestamp"),
        }


__all__ = ["HistoryStore"]