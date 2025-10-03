# MariaDB Query Optimizer + Claude Agents

## Overview
Claude-powered FastAPI service that analyzes, optimizes, validates, and estimates the cost of MariaDB SQL queries. The backend orchestrates four specialized agents and now persists every interaction so you can review history and service health.

## Prerequisites
- **Python**: 3.12 or newer
- **MariaDB**: Optional for running the agents, but required for end-to-end validation of generated SQL
- **Anthropic API access**: Provide a valid Claude API key

## Setup
1. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy environment template and populate required values:
   ```bash
   cp .env.example .env
   ```
4. Start the FastAPI app:
   ```bash
   uvicorn main:app --reload
   ```

## Environment Configuration
- **CLAUDE_API_KEY**: Primary Anthropic key used by all agents (required)
- **CLAUDE_MODEL**: Override the default Claude model name (optional)
- **DB_HOST / DB_PORT / DB_USER / DB_PASS / DB_NAME**: MariaDB connection details for validation scenarios (optional)
- **LOG_LEVEL / API_HOST / API_PORT / SANDBOX_ONLY**: Miscellaneous runtime toggles (optional)

## Running the API
1. Ensure `.env` is configured with at least `CLAUDE_API_KEY`.
2. Launch the service with `uvicorn main:app --reload`.
3. Visit `http://127.0.0.1:8000/docs` for interactive Swagger UI.

## API Endpoints
### Core agent endpoints
- **POST /analyze**: General query analysis and optimization suggestions.
- **POST /optimize**: Returns a rewritten SQL statement and rationale.
- **POST /analyze-schema**: Evaluates schema definition statements.
- **POST /estimate-cost**: Generates execution cost insights via `CostAdvisor`.
- **POST /validate-query**: Performs logical and compatibility checks with MariaDB.

### Supporting endpoints
- **GET /**: Health splash that confirms the service is running.
- **GET /status**: Lightweight heartbeat with version metadata.
- **GET /history?limit=N**: Returns the `N` most recent interactions recorded by the JSONL-backed history store (default `10`). Each entry includes timestamp, endpoint, request payload, and response summary.
- **GET /metrics**: Aggregated counts, timestamps, average response durations, and agent-level status flags suitable for dashboards or uptime monitors.

## Sample Workflows
### 1. Query performance review
1. Submit the SQL to `/analyze`:
   ```bash
   curl -X POST http://127.0.0.1:8000/analyze \
     -H "Content-Type: application/json" \
     -d '{"sql_query": "SELECT * FROM orders o JOIN customers c ON o.customer_id = c.id WHERE o.created_at >= "2024-01-01""}'
   ```
2. Paste the recommendations into `/optimize` to receive a rewritten query with rationale.
3. Call `/estimate-cost` with the same SQL to obtain a structured cost breakdown from the `CostAdvisor`.
4. Review the consolidated feedback with `GET /history?limit=5`.

### 2. Schema change dry run
1. Provide a DDL statement to `/analyze-schema` for compatibility feedback.
2. Run `/validate-query` to surface semantic issues, error codes, or missing indexes.
3. Monitor service health by querying `/metrics` during the evaluation window.

### 3. Nightly insight snapshot
1. Schedule recurring jobs that hit `/optimize` and `/estimate-cost` for critical queries.
2. Aggregate historical results by pulling `/history?limit=50` and feeding into your reporting pipeline.
3. Use `/metrics` to verify that all agents responded without errors.

## Testing
Run automated tests (including history persistence coverage) with:
```bash
pytest
```
Tests stub the Anthropic client, so they run without network access or live API keys.

## Data Persistence
- **History file**: Interactions are appended to `data/history.jsonl` (ignored by version control).
- **Thread safety**: `HistoryStore` synchronizes access so multiple requests can log safely.

## Frontend
Static assets in `frontend/` offer a basic browser UI that proxies the same endpoints. Launch the backend first, then open `frontend/index.html` in a modern browser for manual testing.