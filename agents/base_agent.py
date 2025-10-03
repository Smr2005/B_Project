"""Common functionality shared by Claude-powered agents."""

import os
from anthropic import Anthropic

DEFAULT_MODEL = "claude-3-haiku-20240307"


class BaseAgent:
    """Provide a pre-configured Anthropic client for derived agents."""

    def __init__(self) -> None:
        api_key = os.getenv("CLAUDE_API_KEY")
        if not api_key:
            raise ValueError("❌ CLAUDE_API_KEY environment variable is not set.")

        self.client = Anthropic(api_key=api_key)
        self.model_name = os.getenv("CLAUDE_MODEL", DEFAULT_MODEL)


__all__ = ["BaseAgent", "DEFAULT_MODEL"]