"""Tests for the split_optimizer_output helper."""

import importlib
import os
from types import SimpleNamespace

import pytest

# Ensure the BaseAgent initialization succeeds during module import
os.environ.setdefault("CLAUDE_API_KEY", "test-key")

import agents.base_agent as base_agent_module


class _FakeMessages:
    def create(self, **kwargs):
        # Return an empty response so production code can proceed.
        return SimpleNamespace(content=[SimpleNamespace(text="")])


class _FakeAnthropic:
    def __init__(self, api_key: str):
        self.messages = _FakeMessages()


# Patch Anthropic client before importing the FastAPI app module
base_agent_module.Anthropic = _FakeAnthropic

main = importlib.import_module("main")
split_optimizer_output = main.split_optimizer_output


@pytest.mark.parametrize(
    "raw_output, expected_query, expected_rationale",
    [
        (
            """
            Optimized SQL Query:
            SELECT * FROM orders;

            Rationale:
            - Semantics: No change needed.
            - Performance: Query already optimal.
            """,
            "SELECT * FROM orders;",
            "- Semantics: No change needed.\n- Performance: Query already optimal.",
        ),
        (
            """
            Optimized SQL Query:
            SELECT * FROM users;
            """,
            "SELECT * FROM users;",
            "",
        ),
        (
            """
            SELECT * FROM raw_text;

            Rationale:
            - MariaDB Compatibility: Query is valid.
            """,
            "SELECT * FROM raw_text;",
            "- MariaDB Compatibility: Query is valid.",
        ),
        ("", "", ""),
        (None, "", ""),
    ],
)
def test_split_optimizer_output(raw_output, expected_query, expected_rationale):
    """Ensure split_optimizer_output parses the agent response correctly."""
    query, rationale = split_optimizer_output(raw_output)
    assert query == expected_query
    assert rationale == expected_rationale