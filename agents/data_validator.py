import os
from anthropic import Anthropic

class DataValidator:
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))

    def validate_query(self, sql_query: str) -> str:
        """Validate query correctness and safety using Claude."""
        prompt = f"""
        You are a MariaDB Data Validator.
        Validate the following SQL query for:
        - Syntax errors
        - Risk of SQL injection
        - Risk of accidental data loss
        - Whether WHERE conditions are too broad or missing
        - Security vulnerabilities

        SQL Query:
        {sql_query}

        Validation Report:
        """

        try:
            response = self.client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=500,
                temperature=0,
                system="You are a MariaDB SQL validation and security expert.",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            return response.content[0].text.strip()

        except Exception as e:
            return f"Error in validation: {str(e)}"
