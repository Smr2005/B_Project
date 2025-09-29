import os
from anthropic import Anthropic

class SchemaAdvisor:
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))

    def analyze_schema(self, schema_sql: str) -> str:
        """Analyze schema and suggest improvements using Claude."""
        prompt = f"""
        You are a MariaDB Schema Design Advisor.
        Review the schema below and recommend:
        - Indexing improvements
        - Normalization or denormalization opportunities
        - Partitioning or sharding if necessary
        - Data type optimizations

        Schema:
        {schema_sql}

        Suggestions:
        """

        try:
            response = self.client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=500,
                temperature=0,
                system="You are an expert in MariaDB schema design and optimization.",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            return response.content[0].text.strip()

        except Exception as e:
            return f"Error in schema analysis: {str(e)}"
