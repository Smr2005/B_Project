import base64
from pathlib import Path
from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv
from agents import QueryOptimizer, SchemaAdvisor, CostSaver, DataValidator
from utils import HistoryStore

# Load environment variables from .env file if present
load_dotenv()

# FastAPI instance
app = FastAPI(title="MariaDB Query Optimizer API 🚀")

# Persistent history store
history_store = HistoryStore(Path(__file__).resolve().parent / "data" / "history.jsonl")

# Serve frontend assets
FRONTEND_DIR = Path(__file__).resolve().parent / "frontend"
app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="static")

# Initialize agents
try:
    query_optimizer = QueryOptimizer()
    schema_advisor = SchemaAdvisor()
    cost_saver = CostSaver()
    data_validator = DataValidator()
except ValueError as exc:
    # Delay failures until runtime so frontend can display useful message
    query_optimizer = None
    schema_advisor = None
    cost_saver = None
    data_validator = None
    initialization_error = str(exc)
else:
    initialization_error = None


@app.get("/status")
def status_check():
    if initialization_error:
        raise HTTPException(status_code=500, detail=initialization_error)
    return {"status": "ok"}


@app.get("/history")
def recent_history(limit: int = 20):
    if initialization_error:
        raise HTTPException(status_code=500, detail=initialization_error)
    return {"entries": history_store.get_recent(limit=limit)}


@app.get("/metrics")
def service_metrics():
    if initialization_error:
        raise HTTPException(status_code=500, detail=initialization_error)
    metrics = history_store.metrics()
    metrics.update({
        "agents": {
            "query_optimizer": query_optimizer is not None,
            "schema_advisor": schema_advisor is not None,
            "cost_saver": cost_saver is not None,
            "data_validator": data_validator is not None,
        }
    })
    return metrics

# Request models
class QueryRequest(BaseModel):
    sql_query: str

class SchemaRequest(BaseModel):
    schema_sql: str


def split_optimizer_output(raw_output: str) -> tuple[str, str]:
    """Split the optimizer response into SQL and rationale sections."""
    if not isinstance(raw_output, str):
        return "", ""

    text = raw_output.strip()
    if not text:
        return "", ""

    if "Optimized SQL Query:" in text:
        _, remainder = text.split("Optimized SQL Query:", 1)
        if "Rationale:" in remainder:
            query_text, rationale_text = remainder.split("Rationale:", 1)
            return query_text.strip(), rationale_text.strip()
        return remainder.strip(), ""

    if "Rationale:" in text:
        query_text, rationale_text = text.split("Rationale:", 1)
        return query_text.strip(), rationale_text.strip()

    return text, ""


@app.get("/")
def root():
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/favicon.ico")
def favicon():
    # Favicon rendered from base64-encoded PNG (a small rocket icon)
    favicon_base64 = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAABhklEQVR4nI2TsUoDQRCFv1M7KJna"
        "Nz/gIGhuLgJBLyWg9mBTsYmLhIsrJ2auksBO52U7CJv5DyKkhOUhY2EJa5baYvXNo3nAPE9eM5l3"
        "Z/fc7BI62TB7RdRB18ABrtFuiFpvNj21mxPkzTilN2Oa75iGrS2B3JD2zRcDQ3jqI9rYwnSxT8a0"
        "6+kn/mxNOOu0cYd75iS1MQnnelOyO2M2IPaMVp3srJVaMKp6whHQExbYTtBwudO9LCn43/ZwVhId"
        "qLzbw0GEIuwKOPp6asHPVuZdyK7RJdrPxG2yRdp04qj81AgIgxEq9bM58Ctkt42gHe0QQ5rqILFc"
        "7XRHIwBsYmYoSRTV41h5G5ArqIYmZwD6tSqk5pq4A/1tT41RadvAciSH+HZX1oAwLAX2sf49P7jp"
        "wxrniMmxjhJbVOBTHrojiyKeHYF1YgfP3Bz5gmnu69Jw3kforuM/b8gIT1NhYsNyyKWeL6FFR9Hn"
        "sNa2M0kVQZGMj2ScZm1BFGcVjqAiqdmtYTODmZojpqpnEs27ScNrqTYhEdAql1LKYHjfbicRfFvL"
        "tZFbXNcuF3KRtOsd6/gHzrkZU4af35kAAAAASUVORK5CYII="
    )
    favicon_bytes = base64.b64decode(favicon_base64)
    return Response(content=favicon_bytes, media_type="image/png")


@app.post("/analyze")
def analyze_query(request: QueryRequest):
    if initialization_error:
        raise HTTPException(status_code=500, detail=initialization_error)

    optimized_text = query_optimizer.optimize_query(request.sql_query)
    optimized_query, optimization_rationale = split_optimizer_output(optimized_text)

    query_to_review = optimized_query if optimized_query else request.sql_query

    validation_report = data_validator.validate_query(query_to_review)
    cost_estimation = cost_saver.save_cost({'sql_query': query_to_review})
    schema_suggestions = schema_advisor.analyze_schema(query_to_review)

    response_payload = {
        "original_query": request.sql_query.strip(),
        "optimized_query": optimized_query,
        "optimization_rationale": optimization_rationale,
        "validation_report": validation_report,
        "cost_estimation": cost_estimation,
        "schema_suggestions": schema_suggestions,
    }

    history_store.append({
        "type": "analysis",
        "request": request.dict(),
        "response": response_payload,
    })

    return response_payload


@app.post("/optimize")
def optimize_query(request: QueryRequest):
    if initialization_error:
        raise HTTPException(status_code=500, detail=initialization_error)

    optimized_query = query_optimizer.optimize_query(request.sql_query)
    history_store.append({
        "type": "optimize",
        "request": request.dict(),
        "response": {"optimized_query": optimized_query},
    })
    return {"optimized_query": optimized_query}


@app.post("/analyze-schema")
def analyze_schema(request: SchemaRequest):
    if initialization_error:
        raise HTTPException(status_code=500, detail=initialization_error)

    schema_suggestions = schema_advisor.analyze_schema(request.schema_sql)
    history_store.append({
        "type": "analyze_schema",
        "request": request.dict(),
        "response": {"schema_suggestions": schema_suggestions},
    })
    return {"schema_suggestions": schema_suggestions}


@app.post("/save-cost")
def save_cost(request: QueryRequest):
    if initialization_error:
        raise HTTPException(status_code=500, detail=initialization_error)

    cost_estimation = cost_saver.save_cost({'sql_query': request.sql_query})
    history_store.append({
        "type": "save_cost",
        "request": request.dict(),
        "response": {"cost_estimation": cost_estimation},
    })
    return {"cost_estimation": cost_estimation}


@app.post("/validate-query")
def validate_query(request: QueryRequest):
    if initialization_error:
        raise HTTPException(status_code=500, detail=initialization_error)

    validation_report = data_validator.validate_query(request.sql_query)
    history_store.append({
        "type": "validate_query",
        "request": request.dict(),
        "response": {"validation_report": validation_report},
    })
    return {"validation_report": validation_report}
