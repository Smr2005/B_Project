from .base_agent import BaseAgent


class QueryOptimizer(BaseAgent):
    def __init__(self):
        super().__init__()

    def optimize_query(self, sql_query: str) -> str:
        """Optimize an SQL query using Claude."""
        
        # Detect SQL statement type
        sql_upper = sql_query.strip().upper()
        
        # Determine statement type
        if sql_upper.startswith('CREATE TABLE') or 'CREATE TABLE' in sql_upper:
            statement_type = 'CREATE TABLE'
        elif sql_upper.startswith('CREATE INDEX') or sql_upper.startswith('CREATE UNIQUE INDEX'):
            statement_type = 'CREATE INDEX'
        elif sql_upper.startswith('ALTER TABLE'):
            statement_type = 'ALTER TABLE'
        elif sql_upper.startswith('INSERT'):
            statement_type = 'INSERT'
        elif sql_upper.startswith('UPDATE'):
            statement_type = 'UPDATE'
        elif sql_upper.startswith('DELETE'):
            statement_type = 'DELETE'
        elif sql_upper.startswith('SELECT') or sql_upper.startswith('WITH'):
            statement_type = 'SELECT'
        else:
            statement_type = 'UNKNOWN'
        
        # Universal optimization prompt that works for ALL statement types
        prompt = f"""
        You are a MariaDB optimization expert. Your goal is to SIGNIFICANTLY improve query performance, not just make cosmetic changes.

        The user has provided a SQL statement. Your task is to optimize it while preserving its type and purpose.

        CRITICAL RULES:
        1. **PRESERVE STATEMENT TYPE**: If the input is CREATE TABLE, return optimized CREATE TABLE. If it's SELECT, return optimized SELECT. If it's INSERT, return optimized INSERT, etc.
        2. **DO NOT CHANGE STATEMENT TYPE**: Never convert CREATE TABLE to SELECT, or SELECT to INSERT, etc.
        3. **PRESERVE SEMANTICS - ABSOLUTELY CRITICAL**: The optimized statement MUST produce EXACTLY the same result as the original
           - Same number of rows
           - Same column values in each row
           - Same NULL handling
           - If original has correlated subquery per row, optimization must maintain per-row logic
        4. **AGGRESSIVE OPTIMIZATION**: Make REAL performance improvements, not just cosmetic changes like adding "INNER" to JOIN
        5. **MARIADB COMPATIBILITY**: Ensure all syntax is valid for MariaDB

        Statement Type Detected: {statement_type}

        Optimization Guidelines by Type:

        **For CREATE TABLE:**
        - Optimize data types (use UNSIGNED, appropriate sizes)
        - Add missing indexes for foreign keys and frequently queried columns
        - Add constraints (PRIMARY KEY, FOREIGN KEY, UNIQUE, NOT NULL)
        - Specify ENGINE, CHARSET, COLLATION
        - Add AUTO_INCREMENT where appropriate
        - Remove redundant indexes

        **For SELECT - AGGRESSIVE OPTIMIZATION REQUIRED:**
        
        **CRITICAL: Eliminate Duplicate Subqueries - THIS IS MANDATORY**
        - SCAN THE QUERY: Look for multiple subqueries that query the same table(s) with the same JOIN/WHERE/ORDER BY logic
        - If you find duplicate subqueries (even if they SELECT different columns), you MUST combine them
        - NEVER return the original query if duplicate subqueries exist
        
        **IMPORTANT: Preserve Correlation Logic**
        - If subqueries are CORRELATED (have WHERE clause referencing outer table), the optimization MUST preserve this
        - Use window functions (ROW_NUMBER, RANK) to maintain per-group logic
        - Example Pattern to FIX:
          ```
          SELECT (SELECT col1 FROM t WHERE t.id = outer.id ORDER BY y LIMIT 1),
                 (SELECT col2 FROM t WHERE t.id = outer.id ORDER BY y LIMIT 1)
          FROM outer
          ```
          MUST become (using window functions):
          ```
          SELECT outer.*, derived.col1, derived.col2
          FROM outer
          LEFT JOIN (
            SELECT col1, col2, id,
                   ROW_NUMBER() OVER (PARTITION BY id ORDER BY y DESC) as rn
            FROM t
          ) derived ON outer.id = derived.id AND derived.rn = 1
          ```
        
        **Subquery Optimization:**
        - Replace ALL correlated subqueries with JOINs or derived tables (correlated subqueries execute once per row - extremely slow)
        - Use window functions (ROW_NUMBER, RANK, FIRST_VALUE) to maintain per-group logic
        - For "top N per group" patterns, use ROW_NUMBER() OVER (PARTITION BY ... ORDER BY ...)
        - Move subqueries to FROM clause as derived tables
        - If a subquery appears in SELECT list, convert it to a LEFT JOIN
        - CRITICAL: When using window functions, filter with WHERE rn = 1 in the derived table or in the JOIN condition
        
        **JOIN Optimization:**
        - Use proper join types (INNER, LEFT, RIGHT)
        - Reorder joins for better performance (smaller tables first)
        - Use derived tables to pre-filter data before joining
        
        **Other Optimizations:**
        - Fix LIMIT in IN/EXISTS (use derived tables or window functions)
        - Remove redundant ORDER BY/GROUP BY
        - Use indexes efficiently
        - Avoid SELECT * when specific columns are needed
        - Use UNION ALL instead of UNION when duplicates don't matter
        - Push WHERE conditions into subqueries when possible

        **For INSERT:**
        - Use batch inserts when possible (combine multiple INSERT statements)
        - Optimize INSERT ... SELECT statements
        - Use appropriate locking strategies
        - Consider INSERT IGNORE or ON DUPLICATE KEY UPDATE

        **For UPDATE:**
        - Optimize WHERE clauses for index usage
        - Avoid full table scans
        - Use appropriate JOIN syntax
        - Consider batch updates

        **For DELETE:**
        - Optimize WHERE clauses for index usage
        - Use appropriate JOIN syntax
        - Consider TRUNCATE for full table deletes

        **For ALTER TABLE:**
        - Optimize column definitions
        - Suggest better index strategies
        - Recommend partitioning if applicable

        **For CREATE INDEX:**
        - Optimize index column order
        - Suggest composite indexes
        - Remove redundant indexes

        MariaDB Compatibility Rules:
        - No LIMIT inside IN/EXISTS subqueries (ERROR 1235)
        - Use supported window functions (MariaDB 10.2+)
        - Use supported JSON functions (MariaDB 10.2+)
        - Avoid vendor-specific syntax from other databases

        **MANDATORY PRE-OPTIMIZATION CHECK FOR SELECT QUERIES:**
        Before you respond, you MUST check:
        1. Are there multiple subqueries in the SELECT clause?
        2. Do any of them query the same table(s) with similar logic?
        3. If YES to both, you MUST combine them - returning the original is NOT acceptable
        4. Are the subqueries CORRELATED (reference outer table)? If YES, use window functions with PARTITION BY
        5. VERIFY: Does your optimized query produce the SAME results as the original? Test the logic mentally
        
        When no optimization is possible:
        - Return the original statement unchanged
        - In rationale, explain why it's already optimal
        - DO NOT return the original if there are obvious optimizations like duplicate subqueries

        Input SQL Statement:
        {sql_query}

        Respond using the following format:

        Optimized SQL Query:
        <optimized statement of the SAME TYPE as input with REAL performance improvements>

        Rationale:
        - <bullet 1: SPECIFIC optimization made - e.g., "Combined 2 duplicate correlated subqueries into single LEFT JOIN">
        - <bullet 2: QUANTIFIED performance impact - e.g., "Reduces subquery executions from 2N to 0 (where N = number of customers)">
        - <bullet 3: Technical explanation - e.g., "Original: 2 correlated subqueries execute for each row. Optimized: Single derived table executes once">
        - <bullet 4: Additional recommendations if any>
        
        **IMPORTANT**: If you only made cosmetic changes (like adding INNER keyword), that means you MISSED the real optimization. Go back and find it.
        """

        try:
            # Use more tokens for complex statements that need detailed optimization
            if statement_type in ['CREATE TABLE', 'ALTER TABLE', 'CREATE INDEX']:
                max_tokens = 1500
            elif statement_type == 'SELECT':
                max_tokens = 1500  # SELECT queries need complex optimization with detailed explanations
            else:
                max_tokens = 1000
            
            response = self.client.messages.create(
                model=self.model_name,
                max_tokens=max_tokens,
                temperature=0,
                system="You are a world-class MariaDB query optimizer.",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            return response.content[0].text.strip()

        except Exception as e:
            return f"Error during optimization: {str(e)}"
