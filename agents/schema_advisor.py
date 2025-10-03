from .base_agent import BaseAgent


class SchemaAdvisor(BaseAgent):
    def __init__(self):
        super().__init__()

    def analyze_schema(self, schema_sql: str) -> str:
        """Analyze schema and suggest improvements using Claude."""
        prompt = f"""
        You are a MariaDB Schema Design Advisor.

        Evaluation Checklist:
        - Indexing: Identify missing, redundant, or composite indexes and tie each recommendation to specific query patterns.
        - Data Modeling: Flag normalization/denormalization opportunities, foreign key integrity gaps, and partition/sharding strategies when justified by data volume.
        - Data Types: Suggest optimal data types (length, unsigned, charset/collation) and note storage/performance trade-offs.
        - MariaDB Compatibility: Call out version-dependent or unsupported features (e.g., functional indexes, CHECK constraints before 10.2, invisible indexes) and offer supported alternatives.
        - Operational Considerations: Mention replication, backup, and maintenance implications when relevant (e.g., large blob columns, heavy write tables).

        Schema:
        {schema_sql}

        Structured Recommendations:
        - Indexing: <details>
        - Data Modeling: <details>
        - Data Types: <details>
        - MariaDB Compatibility: <issues + alternatives>
        - Operational Notes: <details or "None">
        """

        try:
            response = self.client.messages.create(
                model=self.model_name,
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
