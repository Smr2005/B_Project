from .base_agent import BaseAgent

class DataValidator(BaseAgent):
    def __init__(self):
        super().__init__()

    def validate_query(self, sql_query: str) -> str:
        """
        Validate query correctness and safety:
        - Syntax errors
        - SQL injection risk
        - Risk of accidental data loss
        - Too broad WHERE conditions
        - Security vulnerabilities
        """
        prompt = f"""
        You are a MariaDB Data Validator.

        Tasks:
        1. Inspect the query for syntax errors, security risks, and unsafe data modifications.
        2. Highlight constructs MariaDB cannot execute (e.g., recursive CTE features before 10.2, vendor-specific syntax) and provide compliant rewrites.
        3. If `LIMIT` or `OFFSET` appears inside an `IN/EXISTS` predicate, state that it is forbidden in MariaDB and show a derived-table rewrite that preserves the same key set.
        4. Flag rewrites that collapse set-based membership (e.g., converting `IN`/`EXISTS` into scalar comparisons) because they can drop rows; suggest using derived tables or joins that retain the full result set.
        5. Call out overly broad WHERE conditions, missing safeguards (transactions, `WHERE` on UPDATE/DELETE), or injection risks.

        SQL Query:
        {sql_query}

        Structured Validation Report:
        - Syntax Compliance: <pass/fail + notes>
        - MariaDB Compatibility: <issues + fixes>
        - Safety Assessment: <risks + mitigations>
        - Recommended Rewrites: <bullet list or "None">
        """

        try:
            response = self.client.messages.create(
                model=self.model_name,
                max_tokens=500,
                temperature=0,
                system="You are a MariaDB SQL validation and security expert.",
                messages=[{"role": "user", "content": prompt}],
            )
            return response.content[0].text.strip()
        except Exception as e:
            return f"❌ Error in validation: {str(e)}"
