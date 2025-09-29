from agents.query_optimizer import QueryOptimizer
from agents.schema_advisor import SchemaAdvisor
from agents.cost_advisor import CostAdvisor
from agents.data_validator import DataValidator

def main():
    # Example input query
    sql_query = "SELECT * FROM employees WHERE department_id = 10;"

    # Example schema
    schema_sql = """
    CREATE TABLE employees (
        id INT PRIMARY KEY,
        department_id INT,
        name VARCHAR(100),
        salary DECIMAL(10,2)
    );
    """

    optimizer = QueryOptimizer()
    schema_advisor = SchemaAdvisor()
    cost_advisor = CostAdvisor()
    validator = DataValidator()

    print("🔹 Original Query:")
    print(sql_query)

    print("\n🔹 Optimized Query:")
    print(optimizer.optimize_query(sql_query))

    print("\n🔹 Schema Advice:")
    print(schema_advisor.analyze_schema(schema_sql))

    print("\n🔹 Cost Advice:")
    print(cost_advisor.estimate_cost(sql_query))

    print("\n🔹 Validation Report:")
    print(validator.validate_query(sql_query))

if __name__ == "__main__":
    main()
