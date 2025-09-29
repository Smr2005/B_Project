import os
from anthropic import Anthropic

class CostAdvisor:
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))

    def estimate_cost(self, sql_query: str) -> str:
        """Estimate query cost and give optimization advice using Claude."""
        prompt = f"""
        You are a MariaDB Cost Advisor.
        Estimate the cost of running this SQL query.
        - Identify expensive operations (joins, scans, sorts).
        - Suggest indexing or rewriting improvements to reduce cost.
        
        SQL Query:
        {sql_query}

        Cost & Optimization Advice:
        """

        try:
            response = self.client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=500,
                temperature=0,
                system="You are a MariaDB execution plan and cost optimization expert.",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            return response.content[0].text.strip()

        except Exception as e:
            return f"Error in cost estimation: {str(e)}"
