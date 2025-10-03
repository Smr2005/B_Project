"""Tests for the HistoryStore persistence helper."""

from __future__ import annotations

from pathlib import Path

import pytest

from utils.history_store import HistoryStore


@pytest.fixture()
def temp_history(tmp_path: Path) -> HistoryStore:
    store = HistoryStore(tmp_path / "history.jsonl")
    return store


def test_append_creates_file(temp_history: HistoryStore):
    temp_history.append({"type": "test", "payload": 1})
    assert temp_history.storage_path.exists()
    lines = [line for line in temp_history.storage_path.read_text(encoding="utf-8").splitlines() if line]
    assert len(lines) == 1


def test_get_recent_returns_ordered_entries(temp_history: HistoryStore):
    for idx in range(5):
        temp_history.append({"type": "test", "payload": idx})

    recent = temp_history.get_recent(limit=3)
    assert len(recent) == 3
    assert [entry["payload"] for entry in recent] == [2, 3, 4]


def test_metrics_reports_counts(temp_history: HistoryStore):
    assert temp_history.metrics()["total_entries"] == 0

    temp_history.append({"type": "test", "payload": 1})
    temp_history.append({"type": "test", "payload": 2})

    metrics = temp_history.metrics()
    assert metrics["total_entries"] == 2
    assert metrics["first_run_at"] is not None
    assert metrics["last_run_at"] is not None