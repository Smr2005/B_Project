from .base_agent import BaseAgent


class CostSaver(BaseAgent):
    def __init__(self):
        super().__init__()

    def save_cost(self, inputs: dict) -> str:
        """
        Reduce execution and storage costs via slow logs, caching, archiving, compression.
        - Analyze slow query logs for patterns.
        - Suggest caching strategies.
        - Recommend archiving/compression for old data.
        - Identify unused indexes, redundant data.
        """
        sql_query = inputs.get('sql_query', '')
        slow_logs = inputs.get('slow_logs', '')
        storage_stats = inputs.get('storage_stats', '')
        query_history = inputs.get('query_history', '')

        prompt = f"""
        You are a MariaDB Cost Saver.

        Analysis Goals:
        - Analyze slow query logs for recurring expensive patterns and suggest optimizations.
        - Review storage statistics to identify opportunities for archiving, compression, or purging unused data.
        - Recommend caching strategies (e.g., query cache, application-level caching) to reduce I/O.
        - Identify unused or redundant indexes that increase storage costs without benefit.
        - Suggest cost-effective alternatives for high-cost operations (e.g., partitioning, summary tables).

        Inputs:
        - SQL Query: {sql_query}
        - Slow Logs: {slow_logs}
        - Storage Stats: {storage_stats}
        - Query History: {query_history}

        Structured Cost-Saving Report:
        - Slow Log Analysis: <patterns + recommendations>
        - Storage Optimization: <archiving/compression suggestions>
        - Caching Opportunities: <strategies>
        - Index Review: <unused/redundant indexes>
        - Overall Cost Reduction Plan: <prioritized actions>
        """

        try:
            response = self.client.messages.create(
                model=self.model_name,
                max_tokens=500,
                temperature=0,
                system="You are a MariaDB execution plan and cost optimization expert.",
                messages=[{"role": "user", "content": prompt}],
            )

            return response.content[0].text.strip()

        except Exception as e:
            return f"❌ Error in cost estimation: {str(e)}"
