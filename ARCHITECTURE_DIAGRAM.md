# 🏛️ MariaDB Query Optimizer - Architecture Diagram

## 🎯 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│                           🌐 PRESENTATION LAYER                             │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │                                                                         │ │
│  │                         Web Browser (Client)                           │ │
│  │                                                                         │ │
│  │  ┌─────────────────────────────────────────────────────────────────┐  │ │
│  │  │  HTML (index.html)                                              │  │ │
│  │  │  - Form structure                                               │  │ │
│  │  │  - Result containers                                            │  │ │
│  │  │  - Semantic markup                                              │  │ │
│  │  └─────────────────────────────────────────────────────────────────┘  │ │
│  │                                                                         │ │
│  │  ┌─────────────────────────────────────────────────────────────────┐  │ │
│  │  │  CSS (style.css)                                                │  │ │
│  │  │  - Dark theme with gradients                                    │  │ │
│  │  │  - Glass morphism effects                                       │  │ │
│  │  │  - Responsive design                                            │  │ │
│  │  │  - Animations & transitions                                     │  │ │
│  │  └─────────────────────────────────────────────────────────────────┘  │ │
│  │                                                                         │ │
│  │  ┌─────────────────────────────────────────────────────────────────┐  │ │
│  │  │  JavaScript (script.js)                                         │  │ │
│  │  │  - Event handling                                               │  │ │
│  │  │  - API communication                                            │  │ │
│  │  │  - Dynamic rendering                                            │  │ │
│  │  │  - Prism.js integration                                         │  │ │
│  │  └─────────────────────────────────────────────────────────────────┘  │ │
│  │                                                                         │ │
│  │  ┌─────────────────────────────────────────────────────────────────┐  │ │
│  │  │  External Libraries                                             │  │ │
│  │  │  - Prism.js (syntax highlighting)                               │  │ │
│  │  │  - Font Awesome (icons)                                         │  │ │
│  │  │  - Google Fonts (typography)                                    │  │ │
│  │  └─────────────────────────────────────────────────────────────────┘  │ │
│  │                                                                         │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                      ↕
                            HTTP/REST API (JSON)
                                      ↕
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│                          🚀 APPLICATION LAYER                               │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │                                                                         │ │
│  │                      FastAPI Application (main.py)                     │ │
│  │                                                                         │ │
│  │  ┌─────────────────────────────────────────────────────────────────┐  │ │
│  │  │  Route Handlers                                                 │  │ │
│  │  │                                                                  │  │ │
│  │  │  GET  /              → Serve frontend                           │  │ │
│  │  │  GET  /status        → Health check                             │  │ │
│  │  │  GET  /history       → Get recent analyses                      │  │ │
│  │  │  GET  /metrics       → Usage statistics                         │  │ │
│  │  │  POST /analyze       → Full analysis (main endpoint)            │  │ │
│  │  │  POST /optimize      → Query optimization only                  │  │ │
│  │  │  POST /validate-query → Validation only                         │  │ │
│  │  │  POST /save-cost     → Cost estimation only                     │  │ │
│  │  │  POST /analyze-schema → Schema analysis only                    │  │ │
│  │  │                                                                  │  │ │
│  │  └─────────────────────────────────────────────────────────────────┘  │ │
│  │                                                                         │ │
│  │  ┌─────────────────────────────────────────────────────────────────┐  │ │
│  │  │  Request/Response Models (Pydantic)                             │  │ │
│  │  │                                                                  │  │ │
│  │  │  class QueryRequest(BaseModel):                                 │  │ │
│  │  │      sql_query: str                                             │  │ │
│  │  │                                                                  │  │ │
│  │  │  class SchemaRequest(BaseModel):                                │  │ │
│  │  │      schema_sql: str                                            │  │ │
│  │  │                                                                  │  │ │
│  │  └─────────────────────────────────────────────────────────────────┘  │ │
│  │                                                                         │ │
│  │  ┌─────────────────────────────────────────────────────────────────┐  │ │
│  │  │  Middleware & Configuration                                     │  │ │
│  │  │                                                                  │  │ │
│  │  │  - Static file serving (/static)                                │  │ │
│  │  │  - CORS (if needed)                                             │  │ │
│  │  │  - Error handling                                               │  │ │
│  │  │  - Logging                                                      │  │ │
│  │  │                                                                  │  │ │
│  │  └─────────────────────────────────────────────────────────────────┘  │ │
│  │                                                                         │ │
│  │  ┌─────────────────────────────────────────────────────────────────┐  │ │
│  │  │  Helper Functions                                               │  │ │
│  │  │                                                                  │  │ │
│  │  │  split_optimizer_output(raw_output: str)                        │  │ │
│  │  │    → Separates SQL from rationale                               │  │ │
│  │  │                                                                  │  │ │
│  │  └─────────────────────────────────────────────────────────────────┘  │ │
│  │                                                                         │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                      ↕
                          Direct Python Function Calls
                                      ↕
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│                           🤖 BUSINESS LOGIC LAYER                           │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │                          AI Agent Framework                            │ │
│  │                                                                         │ │
│  │  ┌─────────────────────────────────────────────────────────────────┐  │ │
│  │  │  BaseAgent (base_agent.py)                                      │  │ │
│  │  │                                                                  │  │ │
│  │  │  - Anthropic client initialization                              │  │ │
│  │  │  - API key management                                           │  │ │
│  │  │  - Model configuration                                          │  │ │
│  │  │  - Shared error handling                                        │  │ │
│  │  │                                                                  │  │ │
│  │  │  Properties:                                                    │  │ │
│  │  │    • self.client: Anthropic                                     │  │ │
│  │  │    • self.model_name: str                                       │  │ │
│  │  │                                                                  │  │ │
│  │  └─────────────────────────────────────────────────────────────────┘  │ │
│  │                                    ↑                                    │ │
│  │                                    │ Inherits                           │ │
│  │                    ┌───────────────┼───────────────┐                   │ │
│  │                    │               │               │                   │ │
│  │  ┌─────────────────┴───┐  ┌───────┴────────┐  ┌──┴──────────────┐    │ │
│  │  │  QueryOptimizer     │  │ DataValidator  │  │  CostSaver      │    │ │
│  │  │  (query_optimizer.py)│  │(data_validator.py)│(cost_saver.py)  │    │ │
│  │  │                     │  │                │  │                 │    │ │
│  │  │  optimize_query()   │  │ validate_query()│  │ save_cost()     │    │ │
│  │  │                     │  │                │  │                 │    │ │
│  │  │  • Detects SQL type │  │ • Syntax check │  │ • Cost analysis │    │ │
│  │  │  • Builds prompt    │  │ • Security scan│  │ • Savings tips  │    │ │
│  │  │  • Calls Claude API │  │ • Compatibility│  │ • Performance   │    │ │
│  │  │  • Returns optimized│  │ • Safety check │  │ • Index review  │    │ │
│  │  │                     │  │                │  │                 │    │ │
│  │  │  Token limit: 1500  │  │ Token limit: 500│ │ Token limit: 500│    │ │
│  │  │                     │  │                │  │                 │    │ │
│  │  └─────────────────────┘  └────────────────┘  └─────────────────┘    │ │
│  │                                                                         │ │
│  │  ┌─────────────────────────────────────────────────────────────────┐  │ │
│  │  │  SchemaAdvisor (schema_advisor.py)                              │  │ │
│  │  │                                                                  │  │ │
│  │  │  analyze_schema()                                               │  │ │
│  │  │                                                                  │  │ │
│  │  │  • Indexing recommendations                                     │  │ │
│  │  │  • Data modeling suggestions                                    │  │ │
│  │  │  • Data type optimization                                       │  │ │
│  │  │  • MariaDB compatibility                                        │  │ │
│  │  │                                                                  │  │ │
│  │  │  Token limit: 500                                               │  │ │
│  │  │                                                                  │  │ │
│  │  └─────────────────────────────────────────────────────────────────┘  │ │
│  │                                                                         │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                      ↕
                              Anthropic API Calls
                                      ↕
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│                          🧠 EXTERNAL AI SERVICE                             │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │                                                                         │ │
│  │                    Anthropic Claude API                                │ │
│  │                                                                         │ │
│  │  ┌─────────────────────────────────────────────────────────────────┐  │ │
│  │  │  Model: claude-3-haiku-20240307                                 │  │ │
│  │  │                                                                  │  │ │
│  │  │  Capabilities:                                                  │  │ │
│  │  │  • Natural language understanding                               │  │ │
│  │  │  • SQL query analysis                                           │  │ │
│  │  │  • Optimization recommendations                                 │  │ │
│  │  │  • Context-aware suggestions                                    │  │ │
│  │  │  • Security analysis                                            │  │ │
│  │  │  • Performance estimation                                       │  │ │
│  │  │                                                                  │  │ │
│  │  │  Request Format:                                                │  │ │
│  │  │  {                                                              │  │ │
│  │  │    "model": "claude-3-haiku-20240307",                          │  │ │
│  │  │    "max_tokens": 1500,                                          │  │ │
│  │  │    "temperature": 0,                                            │  │ │
│  │  │    "messages": [{"role": "user", "content": "..."}]            │  │ │
│  │  │  }                                                              │  │ │
│  │  │                                                                  │  │ │
│  │  │  Response Format:                                               │  │ │
│  │  │  {                                                              │  │ │
│  │  │    "content": [{"text": "Optimized SQL Query: ..."}]           │  │ │
│  │  │  }                                                              │  │ │
│  │  │                                                                  │  │ │
│  │  └─────────────────────────────────────────────────────────────────┘  │ │
│  │                                                                         │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                      ↕
                          Direct Python Function Calls
                                      ↕
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│                           💾 DATA ACCESS LAYER                              │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │                                                                         │ │
│  │                    Utility Modules (utils/)                            │ │
│  │                                                                         │ │
│  │  ┌─────────────────────────────────────────────────────────────────┐  │ │
│  │  │  HistoryStore (history_store.py)                                │  │ │
│  │  │                                                                  │  │ │
│  │  │  Purpose: Persistent storage for analysis history               │  │ │
│  │  │                                                                  │  │ │
│  │  │  Methods:                                                       │  │ │
│  │  │    • append(payload: Dict) → None                               │  │ │
│  │  │      - Adds UTC timestamp                                       │  │ │
│  │  │      - Serializes to JSON                                       │  │ │
│  │  │      - Appends to JSONL file (thread-safe)                      │  │ │
│  │  │                                                                  │  │ │
│  │  │    • get_recent(limit: int = 20) → List[Dict]                   │  │ │
│  │  │      - Reads JSONL file                                         │  │ │
│  │  │      - Returns last N entries                                   │  │ │
│  │  │                                                                  │  │ │
│  │  │    • metrics() → Dict[str, Any]                                 │  │ │
│  │  │      - Total entries count                                      │  │ │
│  │  │      - First/last run timestamps                                │  │ │
│  │  │                                                                  │  │ │
│  │  │  Thread Safety:                                                 │  │ │
│  │  │    • Uses threading.Lock()                                      │  │ │
│  │  │    • Atomic file operations                                     │  │ │
│  │  │                                                                  │  │ │
│  │  └─────────────────────────────────────────────────────────────────┘  │ │
│  │                                                                         │ │
│  │  ┌─────────────────────────────────────────────────────────────────┐  │ │
│  │  │  Config (config.py)                                             │  │ │
│  │  │                                                                  │  │ │
│  │  │  Purpose: Configuration management                              │  │ │
│  │  │                                                                  │  │ │
│  │  │  Functions:                                                     │  │ │
│  │  │    • get_connection() → Connection                              │  │ │
│  │  │    • execute_query(query: str) → Results                        │  │ │
│  │  │    • execute_explain(query: str) → Explain                      │  │ │
│  │  │                                                                  │  │ │
│  │  │  Configuration:                                                 │  │ │
│  │  │    • DB_HOST, DB_PORT, DB_USER, DB_PASS, DB_NAME               │  │ │
│  │  │    • ANTHROPIC_API_KEY, CLAUDE_API_KEY                          │  │ │
│  │  │                                                                  │  │ │
│  │  └─────────────────────────────────────────────────────────────────┘  │ │
│  │                                                                         │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                      ↕
                              File System Operations
                                      ↕
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│                           📁 STORAGE LAYER                                  │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │                                                                         │ │
│  │                      File System Storage                               │ │
│  │                                                                         │ │
│  │  ┌─────────────────────────────────────────────────────────────────┐  │ │
│  │  │  data/history.jsonl                                             │  │ │
│  │  │                                                                  │  │ │
│  │  │  Format: JSONL (JSON Lines)                                     │  │ │
│  │  │  - One JSON object per line                                     │  │ │
│  │  │  - Append-only writes                                           │  │ │
│  │  │  - No database required                                         │  │ │
│  │  │                                                                  │  │ │
│  │  │  Structure:                                                     │  │ │
│  │  │  {                                                              │  │ │
│  │  │    "timestamp": "2024-01-15T10:30:00Z",                         │  │ │
│  │  │    "type": "analysis",                                          │  │ │
│  │  │    "request": {"sql_query": "..."},                            │  │ │
│  │  │    "response": {                                                │  │ │
│  │  │      "original_query": "...",                                   │  │ │
│  │  │      "optimized_query": "...",                                  │  │ │
│  │  │      "optimization_rationale": "...",                           │  │ │
│  │  │      "validation_report": "...",                                │  │ │
│  │  │      "cost_estimation": "...",                                  │  │ │
│  │  │      "schema_suggestions": "..."                                │  │ │
│  │  │    }                                                            │  │ │
│  │  │  }                                                              │  │ │
│  │  │                                                                  │  │ │
│  │  │  Benefits:                                                      │  │ │
│  │  │  • Simple and lightweight                                       │  │ │
│  │  │  • Human-readable                                               │  │ │
│  │  │  • Easy to parse and analyze                                    │  │ │
│  │  │  • No database setup required                                   │  │ │
│  │  │  • Append-only for data integrity                               │  │ │
│  │  │                                                                  │  │ │
│  │  └─────────────────────────────────────────────────────────────────┘  │ │
│  │                                                                         │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Component Interaction Diagram

```
┌──────────────┐
│   Browser    │
└──────┬───────┘
       │
       │ 1. HTTP GET /
       ↓
┌──────────────┐
│   FastAPI    │──────→ Serve index.html, style.css, script.js
└──────┬───────┘
       │
       │ 2. User enters SQL query
       │ 3. Clicks "Analyze Query"
       │
       │ 4. HTTP POST /analyze
       │    Body: {"sql_query": "SELECT ..."}
       ↓
┌──────────────────────────────────────────────────────────┐
│                    FastAPI Router                        │
│                                                          │
│  1. Validate request (Pydantic)                          │
│  2. Check initialization status                          │
│  3. Route to agents                                      │
└──────┬───────────────────────────────────────────────────┘
       │
       │ 5. Call query_optimizer.optimize_query()
       ↓
┌──────────────────────────────────────────────────────────┐
│              QueryOptimizer Agent                        │
│                                                          │
│  1. Detect SQL type (SELECT, INSERT, etc.)               │
│  2. Build optimization prompt                            │
│  3. Send to Claude API                                   │
│  4. Receive optimized query + rationale                  │
│  5. Return to FastAPI                                    │
└──────┬───────────────────────────────────────────────────┘
       │
       │ 6. Split output into query and rationale
       ↓
┌──────────────────────────────────────────────────────────┐
│              split_optimizer_output()                    │
│                                                          │
│  1. Split on "Optimized SQL Query:" marker               │
│  2. Split on "Rationale:" marker                         │
│  3. Return (optimized_query, rationale)                  │
└──────┬───────────────────────────────────────────────────┘
       │
       │ 7. Parallel agent execution
       ├─────────────────┬─────────────────┬────────────────┐
       ↓                 ↓                 ↓                ↓
┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│DataValidator │  │  CostSaver   │  │SchemaAdvisor │  │HistoryStore  │
│              │  │              │  │              │  │              │
│validate_query│  │  save_cost   │  │analyze_schema│  │   append     │
└──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘
       │                 │                 │                 │
       │ 8. All agents complete                             │
       └─────────────────┴─────────────────┴─────────────────┘
                         │
                         │ 9. Aggregate results
                         ↓
┌──────────────────────────────────────────────────────────┐
│              Response Aggregation                        │
│                                                          │
│  response_payload = {                                    │
│    "original_query": "...",                              │
│    "optimized_query": "...",                             │
│    "optimization_rationale": "...",                      │
│    "validation_report": "...",                           │
│    "cost_estimation": "...",                             │
│    "schema_suggestions": "..."                           │
│  }                                                       │
└──────┬───────────────────────────────────────────────────┘
       │
       │ 10. Return JSON response
       ↓
┌──────────────┐
│   Browser    │
└──────┬───────┘
       │
       │ 11. Parse JSON
       │ 12. Format SQL with Prism.js
       │ 13. Create visual diagrams
       │ 14. Render results
       │ 15. Apply syntax highlighting
       ↓
┌──────────────┐
│ User views   │
│   results    │
└──────────────┘
```

---

## 🎯 Agent Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    QueryOptimizer Workflow                      │
└─────────────────────────────────────────────────────────────────┘

Input: SQL Query
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ Step 1: Detect Statement Type                                  │
│                                                                 │
│ sql_upper = sql_query.strip().upper()                          │
│                                                                 │
│ if sql_upper.startswith('SELECT'):                             │
│     statement_type = 'SELECT'                                  │
│ elif sql_upper.startswith('INSERT'):                           │
│     statement_type = 'INSERT'                                  │
│ elif sql_upper.startswith('UPDATE'):                           │
│     statement_type = 'UPDATE'                                  │
│ elif sql_upper.startswith('DELETE'):                           │
│     statement_type = 'DELETE'                                  │
│ elif sql_upper.startswith('CREATE TABLE'):                     │
│     statement_type = 'CREATE TABLE'                            │
│ elif sql_upper.startswith('ALTER TABLE'):                      │
│     statement_type = 'ALTER TABLE'                             │
│ elif sql_upper.startswith('CREATE INDEX'):                     │
│     statement_type = 'CREATE INDEX'                            │
│ else:                                                           │
│     statement_type = 'UNKNOWN'                                 │
└─────────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ Step 2: Build Optimization Prompt                              │
│                                                                 │
│ prompt = f"""                                                   │
│ You are a MariaDB optimization expert.                         │
│                                                                 │
│ CRITICAL RULES:                                                │
│ 1. PRESERVE STATEMENT TYPE                                     │
│ 2. DO NOT CHANGE STATEMENT TYPE                                │
│ 3. PRESERVE SEMANTICS - ABSOLUTELY CRITICAL                    │
│ 4. AGGRESSIVE OPTIMIZATION                                     │
│ 5. MARIADB COMPATIBILITY                                       │
│                                                                 │
│ Statement Type: {statement_type}                               │
│                                                                 │
│ [Type-specific optimization guidelines]                        │
│                                                                 │
│ MANDATORY PRE-OPTIMIZATION CHECK:                              │
│ 1. Multiple subqueries in SELECT?                              │
│ 2. Same table(s) with similar logic?                           │
│ 3. If YES, MUST combine them                                   │
│ 4. Are they CORRELATED? Use window functions                   │
│ 5. VERIFY: Same results as original?                           │
│                                                                 │
│ Input SQL: {sql_query}                                         │
│                                                                 │
│ Respond with:                                                  │
│ Optimized SQL Query:                                           │
│ <optimized statement>                                          │
│                                                                 │
│ Rationale:                                                     │
│ - <SPECIFIC optimization>                                      │
│ - <QUANTIFIED impact>                                          │
│ - <Technical explanation>                                      │
│ """                                                            │
└─────────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ Step 3: Send to Claude API                                     │
│                                                                 │
│ response = self.client.messages.create(                        │
│     model=self.model_name,                                     │
│     max_tokens=1500,  # For SELECT queries                     │
│     temperature=0,                                             │
│     system="You are a world-class MariaDB query optimizer.",   │
│     messages=[{"role": "user", "content": prompt}]             │
│ )                                                              │
└─────────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ Step 4: Claude AI Processing                                   │
│                                                                 │
│ • Analyzes query structure                                     │
│ • Detects duplicate subqueries                                 │
│ • Identifies correlation patterns                              │
│ • Applies window function optimization                         │
│ • Verifies semantic equivalence                                │
│ • Calculates performance impact                                │
│ • Generates optimized query                                    │
│ • Writes detailed rationale                                    │
└─────────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ Step 5: Return Response                                        │
│                                                                 │
│ return response.content[0].text.strip()                        │
│                                                                 │
│ Format:                                                        │
│ "Optimized SQL Query:                                          │
│  SELECT ...                                                    │
│                                                                 │
│  Rationale:                                                    │
│  - Combined 2 duplicate subqueries                             │
│  - Reduces executions from 2N to N                             │
│  - Uses window functions"                                      │
└─────────────────────────────────────────────────────────────────┘
    ↓
Output: Optimized Query + Rationale
```

---

## 📊 Data Flow Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      Request Data Flow                          │
└─────────────────────────────────────────────────────────────────┘

User Input (Textarea)
    ↓
JavaScript (script.js)
    ↓ JSON.stringify()
{
  "sql_query": "SELECT c.name, (SELECT ...), (SELECT ...) FROM customers c"
}
    ↓ fetch("/analyze", {method: "POST", body: ...})
HTTP POST Request
    ↓
FastAPI (main.py)
    ↓ Pydantic validation
QueryRequest(sql_query="SELECT ...")
    ↓
QueryOptimizer.optimize_query(sql_query)
    ↓
Claude API Request
{
  "model": "claude-3-haiku-20240307",
  "max_tokens": 1500,
  "messages": [{"role": "user", "content": "You are a MariaDB..."}]
}
    ↓
Claude API Response
{
  "content": [{"text": "Optimized SQL Query: SELECT ... Rationale: ..."}]
}
    ↓
split_optimizer_output(raw_output)
    ↓
(optimized_query, rationale)
    ↓
Parallel Agent Execution
    ├─ DataValidator.validate_query()
    ├─ CostSaver.save_cost()
    └─ SchemaAdvisor.analyze_schema()
    ↓
Response Aggregation
{
  "original_query": "...",
  "optimized_query": "...",
  "optimization_rationale": "...",
  "validation_report": "...",
  "cost_estimation": "...",
  "schema_suggestions": "..."
}
    ↓
HistoryStore.append(payload)
    ↓
data/history.jsonl
{"timestamp": "2024-01-15T10:30:00Z", "type": "analysis", ...}
    ↓
HTTP Response (JSON)
    ↓
JavaScript (script.js)
    ↓ JSON.parse()
    ↓ formatSQLBlock(), createQueryComparisonDiagram(), etc.
    ↓ Prism.highlightAll()
DOM Update (HTML)
    ↓
User Views Results
```

---

## 🔐 Security Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      Security Layers                            │
└─────────────────────────────────────────────────────────────────┘

Layer 1: Environment Protection
    ├─ API keys stored in .env file
    ├─ .env excluded from version control (.gitignore)
    ├─ Environment variables loaded at runtime
    └─ No hardcoded secrets in source code

Layer 2: Input Validation
    ├─ Frontend: Required field validation
    ├─ Backend: Pydantic schema validation
    ├─ Type checking (sql_query: str)
    └─ Automatic sanitization

Layer 3: Safe Query Analysis
    ├─ Queries are analyzed, NOT executed
    ├─ No direct database connection from user input
    ├─ Static analysis only
    └─ No eval() or exec() calls

Layer 4: AI Security Checks
    ├─ DataValidator agent scans for:
    │   ├─ SQL injection patterns
    │   ├─ Unsafe operations
    │   ├─ Missing WHERE clauses
    │   └─ Security vulnerabilities
    └─ Recommendations for safer alternatives

Layer 5: Output Sanitization
    ├─ HTML escaping (escapeText function)
    ├─ No innerHTML with user data
    ├─ Prism.js handles code rendering safely
    └─ No XSS vulnerabilities

Layer 6: API Rate Limiting (Future)
    ├─ Prevent abuse
    ├─ Protect Claude API quota
    └─ Implement request throttling
```

---

## 🎨 Frontend Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Frontend Component Tree                      │
└─────────────────────────────────────────────────────────────────┘

index.html (Root)
│
├─ <head>
│  ├─ Meta tags (charset, viewport)
│  ├─ <title>
│  ├─ <link> style.css
│  ├─ <link> Font Awesome CDN
│  ├─ <link> Google Fonts (Inter, JetBrains Mono)
│  ├─ <link> Prism.js CSS (prism-tomorrow theme)
│  └─ <link> Prism.js line-numbers plugin CSS
│
└─ <body>
   │
   ├─ .header
   │  ├─ .header-content
   │  │  ├─ .logo
   │  │  │  ├─ <i class="fas fa-database">
   │  │  │  └─ <h1>MariaDB Query Optimizer</h1>
   │  │  └─ <p class="subtitle">
   │
   ├─ .container
   │  │
   │  ├─ .input-section
   │  │  ├─ .section-header
   │  │  │  ├─ <i class="fas fa-code">
   │  │  │  └─ <h2>SQL Query Input</h2>
   │  │  └─ <form id="queryForm">
   │  │     ├─ .textarea-wrapper
   │  │     │  ├─ <textarea id="query">
   │  │     │  └─ .textarea-footer
   │  │     │     └─ <span class="hint">
   │  │     └─ <button type="submit" class="analyze-btn">
   │  │
   │  └─ <div id="result" class="results">
   │     │ (Dynamically populated by JavaScript)
   │     │
   │     ├─ .results__section (Query Comparison)
   │     │  ├─ .results__section-header
   │     │  ├─ .visual-comparison
   │     │  │  └─ .comparison-cards
   │     │  │     ├─ .comparison-card--before
   │     │  │     ├─ .comparison-arrow
   │     │  │     └─ .comparison-card--after
   │     │  ├─ .sql-header
   │     │  │  ├─ <h3>Original Query</h3>
   │     │  │  └─ <button class="copy-btn">
   │     │  └─ .sql-code-wrapper
   │     │     └─ <pre class="line-numbers">
   │     │        └─ <code class="language-sql">
   │     │
   │     ├─ .results__section (Optimization Rationale)
   │     │  ├─ .results__section-header
   │     │  ├─ .performance-metrics
   │     │  │  └─ .metrics-grid
   │     │  │     └─ .metric-card (×4)
   │     │  └─ .bullet-list
   │     │     └─ .bullet-item (×N)
   │     │
   │     ├─ .results__section (Validation Report)
   │     │  ├─ .results__section-header
   │     │  └─ .text-block
   │     │
   │     ├─ .results__section (Cost Estimation)
   │     │  ├─ .results__section-header
   │     │  └─ .text-block
   │     │
   │     └─ .results__section (Schema Suggestions)
   │        ├─ .results__section-header
   │        └─ .text-block
   │
   ├─ .footer
   │  └─ .footer-content
   │     ├─ <p>⚡ Powered by Claude AI</p>
   │     └─ .footer-stats
   │        ├─ <span>Lightning Fast</span>
   │        ├─ <span>Secure</span>
   │        └─ <span>AI-Powered</span>
   │
   └─ <scripts>
      ├─ <script src="prism.min.js">
      ├─ <script src="prism-sql.min.js">
      ├─ <script src="prism-line-numbers.min.js">
      └─ <script src="script.js">
```

---

*Architecture Diagram - Last Updated: January 2024*
*For implementation details, see [Complete Project Documentation](COMPLETE_PROJECT_DOCUMENTATION.md)*