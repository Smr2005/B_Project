# 🔄 MariaDB Query Optimizer - Visual Flow Diagrams

## 📊 Complete System Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│                        🌐 USER INTERACTION LAYER                            │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │                                                                         │ │
│  │  👤 User opens browser → http://127.0.0.1:8000                         │ │
│  │                                                                         │ │
│  │  📝 Types SQL Query:                                                   │ │
│  │     SELECT c.name,                                                     │ │
│  │            (SELECT p.name FROM products p ...),                        │ │
│  │            (SELECT p.price FROM products p ...)                        │ │
│  │     FROM customers c;                                                  │ │
│  │                                                                         │ │
│  │  🖱️  Clicks "Analyze Query" button                                     │ │
│  │                                                                         │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                    ↓                                        │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│                        💻 FRONTEND PROCESSING                               │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │  script.js - Event Handler                                            │ │
│  │                                                                         │ │
│  │  1️⃣  Capture form submit event                                         │ │
│  │  2️⃣  Extract SQL query from textarea                                   │ │
│  │  3️⃣  Show loading spinner                                              │ │
│  │  4️⃣  Prepare JSON payload: { "sql_query": "..." }                     │ │
│  │  5️⃣  Send HTTP POST to /analyze endpoint                              │ │
│  │                                                                         │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                    ↓                                        │
│                          fetch("/analyze", {                                │
│                            method: "POST",                                  │
│                            body: JSON.stringify({...})                      │
│                          })                                                 │
│                                    ↓                                        │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│                        🚀 BACKEND ROUTING (FastAPI)                         │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │  main.py - @app.post("/analyze")                                      │ │
│  │                                                                         │ │
│  │  1️⃣  Receive HTTP POST request                                         │ │
│  │  2️⃣  Validate request body with Pydantic                               │ │
│  │  3️⃣  Check initialization status                                       │ │
│  │  4️⃣  Extract sql_query from request                                    │ │
│  │  5️⃣  Route to QueryOptimizer agent                                     │ │
│  │                                                                         │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                    ↓                                        │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│                        🤖 AI AGENT LAYER - STEP 1                           │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │  QueryOptimizer.optimize_query()                                      │ │
│  │                                                                         │ │
│  │  1️⃣  Detect SQL statement type                                         │ │
│  │     sql_upper = sql_query.strip().upper()                             │ │
│  │     if sql_upper.startswith('SELECT'): type = 'SELECT'                │ │
│  │                                                                         │ │
│  │  2️⃣  Build optimization prompt                                         │ │
│  │     - Add CRITICAL RULES                                               │ │
│  │     - Add duplicate subquery detection                                 │ │
│  │     - Add correlation logic preservation                               │ │
│  │     - Add mandatory pre-optimization checklist                         │ │
│  │                                                                         │ │
│  │  3️⃣  Send to Claude API                                                │ │
│  │     response = client.messages.create(                                 │ │
│  │       model="claude-3-haiku-20240307",                                 │ │
│  │       max_tokens=1500,                                                 │ │
│  │       messages=[{"role": "user", "content": prompt}]                   │ │
│  │     )                                                                   │ │
│  │                                                                         │ │
│  │  4️⃣  Receive optimized query + rationale                               │ │
│  │                                                                         │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                    ↓                                        │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │  🧠 Claude AI Processing                                               │ │
│  │                                                                         │ │
│  │  ✅ Scans for duplicate subqueries                                     │ │
│  │  ✅ Detects correlation (WHERE o2.customer_id = c.customer_id)         │ │
│  │  ✅ Applies window function optimization                               │ │
│  │  ✅ Generates: ROW_NUMBER() OVER (PARTITION BY ... ORDER BY ...)       │ │
│  │  ✅ Verifies semantic equivalence                                      │ │
│  │  ✅ Calculates performance impact (2N → N executions)                  │ │
│  │                                                                         │ │
│  │  Returns:                                                               │ │
│  │  "Optimized SQL Query:                                                 │ │
│  │   SELECT c.name, derived.product_name, derived.price                   │ │
│  │   FROM customers c                                                     │ │
│  │   LEFT JOIN (                                                          │ │
│  │     SELECT o2.customer_id, p.name AS product_name, p.price,            │ │
│  │            ROW_NUMBER() OVER (PARTITION BY o2.customer_id              │ │
│  │                               ORDER BY p.price DESC) AS rn             │ │
│  │     FROM products p JOIN orders o2 ON p.product_id = o2.product_id    │ │
│  │   ) derived ON c.customer_id = derived.customer_id AND derived.rn = 1 │ │
│  │                                                                         │ │
│  │   Rationale:                                                           │ │
│  │   - Combined 2 duplicate correlated subqueries into single LEFT JOIN   │ │
│  │   - Reduces subquery executions from 2N to 0 (N = customers)           │ │
│  │   - Uses window function to maintain per-customer logic                │ │
│  │   - 50% reduction in database operations"                              │ │
│  │                                                                         │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                    ↓                                        │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│                        🔧 OUTPUT PROCESSING                                 │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │  split_optimizer_output(raw_output)                                   │ │
│  │                                                                         │ │
│  │  1️⃣  Split on "Optimized SQL Query:" marker                            │ │
│  │  2️⃣  Split on "Rationale:" marker                                      │ │
│  │  3️⃣  Return tuple: (optimized_query, rationale)                        │ │
│  │                                                                         │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                    ↓                                        │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│                        🤖 AI AGENT LAYER - PARALLEL EXECUTION               │
│                                                                             │
│  ┌─────────────────────┐  ┌─────────────────────┐  ┌──────────────────┐  │
│  │  DataValidator      │  │  CostSaver          │  │  SchemaAdvisor   │  │
│  │  .validate_query()  │  │  .save_cost()       │  │  .analyze_schema()│ │
│  │                     │  │                     │  │                  │  │
│  │  Checks:            │  │  Analyzes:          │  │  Reviews:        │  │
│  │  ✅ Syntax errors   │  │  💰 Query cost      │  │  🏗️ Indexes      │  │
│  │  ✅ SQL injection   │  │  💰 Slow patterns   │  │  🏗️ Data types   │  │
│  │  ✅ MariaDB compat  │  │  💰 Storage usage   │  │  🏗️ Constraints  │  │
│  │  ✅ Safety risks    │  │  💰 Cache options   │  │  🏗️ Normalization│ │
│  │  ✅ LIMIT in IN     │  │  💰 Index review    │  │  🏗️ Partitioning │  │
│  │                     │  │                     │  │                  │  │
│  │  Returns:           │  │  Returns:           │  │  Returns:        │  │
│  │  "Syntax: ✅ Pass   │  │  "Cost Analysis:    │  │  "Schema Tips:   │  │
│  │   Compat: ✅ Pass   │  │   - Estimated cost  │  │   - Add index on │  │
│  │   Safety: ✅ Pass"  │  │   - Savings: 40%"   │  │     customer_id" │  │
│  │                     │  │                     │  │                  │  │
│  └─────────────────────┘  └─────────────────────┘  └──────────────────┘  │
│           ↓                         ↓                        ↓             │
│           └─────────────────────────┴────────────────────────┘             │
│                                    ↓                                        │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│                        📦 RESPONSE AGGREGATION                              │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │  main.py - Combine all agent outputs                                  │ │
│  │                                                                         │ │
│  │  response_payload = {                                                  │ │
│  │    "original_query": "SELECT c.name, (SELECT ...), ...",              │ │
│  │    "optimized_query": "SELECT c.name, derived.name, ...",             │ │
│  │    "optimization_rationale": "- Combined 2 duplicate subqueries...",  │ │
│  │    "validation_report": "Syntax: ✅ Pass, Compat: ✅ Pass...",         │ │
│  │    "cost_estimation": "Estimated cost reduction: 40%...",             │ │
│  │    "schema_suggestions": "Add index on customer_id..."                │ │
│  │  }                                                                     │ │
│  │                                                                         │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                    ↓                                        │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│                        💾 HISTORY STORAGE                                   │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │  HistoryStore.append()                                                │ │
│  │                                                                         │ │
│  │  1️⃣  Add UTC timestamp                                                 │ │
│  │  2️⃣  Serialize to JSON                                                 │ │
│  │  3️⃣  Append to data/history.jsonl (thread-safe)                       │ │
│  │                                                                         │ │
│  │  File: data/history.jsonl                                              │ │
│  │  {"timestamp":"2024-01-15T10:30:00Z","type":"analysis",...}           │ │
│  │                                                                         │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                    ↓                                        │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│                        📤 HTTP RESPONSE                                     │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │  FastAPI returns JSON response                                        │ │
│  │                                                                         │ │
│  │  HTTP 200 OK                                                           │ │
│  │  Content-Type: application/json                                        │ │
│  │                                                                         │ │
│  │  {                                                                     │ │
│  │    "original_query": "...",                                            │ │
│  │    "optimized_query": "...",                                           │ │
│  │    "optimization_rationale": "...",                                    │ │
│  │    "validation_report": "...",                                         │ │
│  │    "cost_estimation": "...",                                           │ │
│  │    "schema_suggestions": "..."                                         │ │
│  │  }                                                                     │ │
│  │                                                                         │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                    ↓                                        │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│                        🎨 FRONTEND RENDERING                                │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │  script.js - Render results                                           │ │
│  │                                                                         │ │
│  │  1️⃣  Parse JSON response                                               │ │
│  │  2️⃣  Create visual comparison diagram                                  │ │
│  │     ┌─────────────┐    ➡️     ┌─────────────┐                         │ │
│  │     │   BEFORE    │  -50%     │    AFTER    │                         │ │
│  │     │  15 lines   │           │   8 lines   │                         │ │
│  │     └─────────────┘           └─────────────┘                         │ │
│  │                                                                         │ │
│  │  3️⃣  Format SQL with Prism.js                                          │ │
│  │     <pre><code class="language-sql">                                   │ │
│  │       SELECT c.name, derived.product_name                              │ │
│  │       FROM customers c                                                 │ │
│  │       LEFT JOIN (...)                                                  │ │
│  │     </code></pre>                                                      │ │
│  │                                                                         │ │
│  │  4️⃣  Add copy buttons                                                  │ │
│  │     <button onclick="copyToClipboard('sql-abc123')">                   │ │
│  │       📋 Copy                                                          │ │
│  │     </button>                                                          │ │
│  │                                                                         │ │
│  │  5️⃣  Create performance metrics                                        │ │
│  │     ┌──────────────┐ ┌──────────────┐ ┌──────────────┐               │ │
│  │     │ Index Usage  │ │ Join Optim.  │ │ Subquery Fix │               │ │
│  │     │      ✅      │ │      ✅      │ │      ✅      │               │ │
│  │     └──────────────┘ └──────────────┘ └──────────────┘               │ │
│  │                                                                         │ │
│  │  6️⃣  Format rationale with bullet points                               │ │
│  │     ✓ Combined 2 duplicate correlated subqueries                       │ │
│  │     ✓ Reduces executions from 2N to 0                                  │ │
│  │     ✓ Uses window function for per-customer logic                      │ │
│  │                                                                         │ │
│  │  7️⃣  Apply syntax highlighting                                         │ │
│  │     Prism.highlightAll()                                               │ │
│  │                                                                         │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                    ↓                                        │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│                        👁️ USER VIEWS RESULTS                                │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │                                                                         │ │
│  │  📊 Query Comparison                                                   │ │
│  │  ┌─────────────────────────────────────────────────────────────────┐  │ │
│  │  │  BEFORE: 15 lines  ➡️  -50%  ➡️  AFTER: 8 lines                  │  │ │
│  │  └─────────────────────────────────────────────────────────────────┘  │ │
│  │                                                                         │ │
│  │  📝 Original Query                                    [📋 Copy]        │ │
│  │  ┌─────────────────────────────────────────────────────────────────┐  │ │
│  │  │  SELECT c.name,                                                  │  │ │
│  │  │         (SELECT p.name FROM products p ...),                     │  │ │
│  │  │         (SELECT p.price FROM products p ...)                     │  │ │
│  │  │  FROM customers c;                                               │  │ │
│  │  └─────────────────────────────────────────────────────────────────┘  │ │
│  │                                                                         │ │
│  │  ✨ Optimized Query                                   [📋 Copy]        │ │
│  │  ┌─────────────────────────────────────────────────────────────────┐  │ │
│  │  │  SELECT c.name, derived.product_name, derived.price             │  │ │
│  │  │  FROM customers c                                                │  │ │
│  │  │  LEFT JOIN (                                                     │  │ │
│  │  │    SELECT o2.customer_id, p.name AS product_name, p.price,      │  │ │
│  │  │           ROW_NUMBER() OVER (PARTITION BY o2.customer_id        │  │ │
│  │  │                              ORDER BY p.price DESC) AS rn        │  │ │
│  │  │    FROM products p JOIN orders o2 ON p.product_id = o2.product_id│ │ │
│  │  │  ) derived ON c.customer_id = derived.customer_id AND rn = 1    │  │ │
│  │  └─────────────────────────────────────────────────────────────────┘  │ │
│  │                                                                         │ │
│  │  💡 Optimization Rationale                                             │ │
│  │  ✓ Combined 2 duplicate correlated subqueries into single LEFT JOIN   │ │
│  │  ✓ Reduces subquery executions from 2N to 0 (N = number of customers) │ │
│  │  ✓ Uses window function to maintain per-customer logic                │ │
│  │  ✓ 50% reduction in database operations                               │ │
│  │                                                                         │ │
│  │  ✅ Validation Report                                                  │ │
│  │  ✓ Syntax Compliance: Pass                                            │ │
│  │  ✓ MariaDB Compatibility: Pass                                        │ │
│  │  ✓ Safety Assessment: Pass                                            │ │
│  │                                                                         │ │
│  │  💰 Cost Estimation                                                    │ │
│  │  ✓ Estimated cost reduction: 40%                                      │ │
│  │  ✓ Reduced I/O operations                                             │ │
│  │                                                                         │ │
│  │  🏗️ Schema Suggestions                                                 │ │
│  │  ✓ Add index on orders.customer_id                                    │ │
│  │  ✓ Add index on products.price                                        │ │
│  │                                                                         │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│  🖱️ User can:                                                              │
│  • Click copy buttons to copy SQL queries                                  │
│  • See visual feedback (button turns green ✓)                              │
│  • Read color-coded SQL syntax                                             │
│  • Review all analysis sections                                            │
│  • Submit another query                                                    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Data Flow Summary

```
User Input
    ↓
Frontend (JavaScript)
    ↓
HTTP POST /analyze
    ↓
FastAPI Router
    ↓
┌─────────────────────────────────────────────────────────┐
│                   AI Agent Layer                        │
│                                                         │
│  QueryOptimizer → Claude API → Optimized Query         │
│  DataValidator  → Claude API → Validation Report       │
│  CostSaver      → Claude API → Cost Estimation         │
│  SchemaAdvisor  → Claude API → Schema Suggestions      │
│                                                         │
└─────────────────────────────────────────────────────────┘
    ↓
Response Aggregation
    ↓
History Storage (JSONL)
    ↓
JSON Response
    ↓
Frontend Rendering (Prism.js)
    ↓
User Views Results
```

---

## ⏱️ Timing Diagram

```
Time (seconds)
0.0  │ User clicks "Analyze Query"
     │
0.1  │ Frontend sends POST request
     │
0.2  │ FastAPI receives request
     │
0.3  │ QueryOptimizer starts
     │
2.5  │ QueryOptimizer completes ✓
     │
2.6  │ Parallel execution starts:
     │   ├─ DataValidator
     │   ├─ CostSaver
     │   └─ SchemaAdvisor
     │
4.5  │ All agents complete ✓
     │
4.6  │ Response aggregation
     │
4.7  │ History storage
     │
4.8  │ JSON response sent
     │
4.9  │ Frontend receives response
     │
5.0  │ Prism.js syntax highlighting
     │
5.2  │ Results displayed to user ✓
```

---

## 🎯 Key Performance Metrics

| Metric | Value | Notes |
|--------|-------|-------|
| **Total Response Time** | 5-8 seconds | Full analysis with all agents |
| **Query Optimization** | 2-4 seconds | Most time-consuming step |
| **Validation** | 1-2 seconds | Fast syntax checking |
| **Cost Estimation** | 1-2 seconds | Lightweight analysis |
| **Schema Analysis** | 2-3 seconds | Depends on complexity |
| **Frontend Rendering** | 0.2-0.5 seconds | Prism.js highlighting |
| **History Storage** | <0.1 seconds | Append-only JSONL |

---

## 🔐 Security Flow

```
┌─────────────────────────────────────────────────────────┐
│  1. User Input                                          │
│     - SQL query entered in textarea                     │
│     - No direct database execution                      │
└─────────────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────────┐
│  2. Frontend Validation                                 │
│     - Required field check                              │
│     - Basic input sanitization                          │
└─────────────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────────┐
│  3. Backend Validation (Pydantic)                       │
│     - Type checking                                     │
│     - Schema validation                                 │
│     - Automatic sanitization                            │
└─────────────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────────┐
│  4. AI Analysis (No Execution)                          │
│     - Query is analyzed, NOT executed                   │
│     - No database connection from user input            │
│     - Safe static analysis only                         │
└─────────────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────────┐
│  5. Security Checks (DataValidator)                     │
│     - SQL injection pattern detection                   │
│     - Unsafe operation warnings                         │
│     - Security recommendations                          │
└─────────────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────────┐
│  6. Safe Response                                       │
│     - Sanitized output                                  │
│     - No sensitive data exposure                        │
│     - Escaped HTML/JavaScript                           │
└─────────────────────────────────────────────────────────┘
```

---

## 📊 Component Interaction Matrix

```
┌──────────────────┬─────────┬─────────┬─────────┬─────────┬─────────┐
│                  │ Frontend│ FastAPI │ Agents  │ Claude  │ Storage │
├──────────────────┼─────────┼─────────┼─────────┼─────────┼─────────┤
│ Frontend         │    -    │  HTTP   │    -    │    -    │    -    │
│ FastAPI          │  HTTP   │    -    │  Direct │    -    │  Direct │
│ Agents           │    -    │  Direct │    -    │   API   │    -    │
│ Claude API       │    -    │    -    │   API   │    -    │    -    │
│ Storage          │    -    │  Direct │    -    │    -    │    -    │
└──────────────────┴─────────┴─────────┴─────────┴─────────┴─────────┘

Legend:
- HTTP: REST API communication
- Direct: Python function calls
- API: External API calls
- "-": No direct interaction
```

---

## 🎨 UI Component Hierarchy

```
index.html
│
├── <head>
│   ├── style.css (styling)
│   ├── Font Awesome (icons)
│   ├── Google Fonts (Inter, JetBrains Mono)
│   └── Prism.js (syntax highlighting)
│
└── <body>
    │
    ├── .header
    │   ├── .logo
    │   │   ├── <i> (database icon)
    │   │   └── <h1> (title)
    │   └── .subtitle
    │
    ├── .container
    │   │
    │   ├── .input-section
    │   │   └── #queryForm
    │   │       ├── <textarea#query>
    │   │       └── <button> (Analyze Query)
    │   │
    │   └── #result (dynamically populated)
    │       │
    │       ├── .results__section (Query Comparison)
    │       │   ├── .visual-comparison
    │       │   ├── .sql-header + .copy-btn
    │       │   └── .sql-code-wrapper
    │       │       └── <pre><code.language-sql>
    │       │
    │       ├── .results__section (Optimization Rationale)
    │       │   ├── .performance-metrics
    │       │   └── .bullet-list
    │       │       └── .bullet-item (with icons)
    │       │
    │       ├── .results__section (Validation Report)
    │       │   └── .validation-cards
    │       │
    │       ├── .results__section (Cost Estimation)
    │       │   └── .text-block
    │       │
    │       └── .results__section (Schema Suggestions)
    │           └── .text-block
    │
    ├── .footer
    │   └── .footer-content
    │
    └── <scripts>
        ├── prism.min.js
        ├── prism-sql.min.js
        └── script.js
```

---

## 🔄 State Management

```
Application State Flow:

┌─────────────────────────────────────────────────────────┐
│  Initial State                                          │
│  - Form: Empty                                          │
│  - Results: Hidden                                      │
│  - Button: Enabled                                      │
└─────────────────────────────────────────────────────────┘
                    ↓ (User types query)
┌─────────────────────────────────────────────────────────┐
│  Input State                                            │
│  - Form: Filled                                         │
│  - Results: Hidden                                      │
│  - Button: Enabled                                      │
└─────────────────────────────────────────────────────────┘
                    ↓ (User clicks Analyze)
┌─────────────────────────────────────────────────────────┐
│  Loading State                                          │
│  - Form: Disabled                                       │
│  - Results: Loading spinner                             │
│  - Button: Disabled                                     │
└─────────────────────────────────────────────────────────┘
                    ↓ (API responds)
┌─────────────────────────────────────────────────────────┐
│  Success State                                          │
│  - Form: Enabled                                        │
│  - Results: Displayed with data                         │
│  - Button: Enabled                                      │
│  - Copy buttons: Interactive                            │
└─────────────────────────────────────────────────────────┘
                    ↓ (User clicks Copy)
┌─────────────────────────────────────────────────────────┐
│  Copy Feedback State                                    │
│  - Copy button: Green with checkmark                    │
│  - Text: Copied to clipboard                            │
│  - Duration: 2 seconds                                  │
└─────────────────────────────────────────────────────────┘
                    ↓ (Timeout)
┌─────────────────────────────────────────────────────────┐
│  Ready State                                            │
│  - Form: Enabled                                        │
│  - Results: Still displayed                             │
│  - Button: Enabled                                      │
│  - Copy buttons: Reset to original                      │
└─────────────────────────────────────────────────────────┘
```

---

*This visual flow diagram complements the Complete Project Documentation*
*Last Updated: January 2024*