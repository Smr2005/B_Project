import os
from anthropic import Anthropic

class QueryOptimizer:
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))

    def optimize_query(self, sql_query: str) -> str:
        """Optimize an SQL query using Claude."""
        prompt = f"""
        You are a MariaDB Query Optimizer expert.
        Rewrite and optimize the given SQL query for best performance.
        Apply indexing, JOIN strategies, subquery optimizations, 
        and avoid full table scans if possible.

        Input SQL Query:
        {sql_query}

        Optimized SQL Query:
        """

        try:
            response = self.client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=500,
                temperature=0,
                system="You are a world-class MariaDB query optimizer.",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            return response.content[0].text.strip()

        except Exception as e:
            return f"Error during optimization: {str(e)}"
