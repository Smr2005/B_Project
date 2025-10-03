# 🚀 MariaDB Query Optimizer - Quick Reference Guide

## 📋 Table of Contents
- [Quick Start](#quick-start)
- [API Endpoints](#api-endpoints)
- [File Structure](#file-structure)
- [Key Functions](#key-functions)
- [Configuration](#configuration)
- [Common Commands](#common-commands)
- [Troubleshooting](#troubleshooting)

---

## ⚡ Quick Start

```bash
# 1. Setup
cd /Users/hmg/Documents/newpro
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Configure
cp .env.example .env
echo "CLAUDE_API_KEY=your_key_here" >> .env

# 3. Run
uvicorn main:app --reload --host 127.0.0.1 --port 8000

# 4. Access
open http://127.0.0.1:8000
```

---

## 🌐 API Endpoints

### Main Endpoints

| Endpoint | Method | Purpose | Request | Response |
|----------|--------|---------|---------|----------|
| `/` | GET | Frontend UI | - | HTML page |
| `/analyze` | POST | Full analysis | `{"sql_query": "..."}` | Complete analysis |
| `/optimize` | POST | Optimize only | `{"sql_query": "..."}` | Optimized query |
| `/validate-query` | POST | Validate only | `{"sql_query": "..."}` | Validation report |
| `/save-cost` | POST | Cost analysis | `{"sql_query": "..."}` | Cost estimation |
| `/analyze-schema` | POST | Schema analysis | `{"schema_sql": "..."}` | Schema suggestions |

### Utility Endpoints

| Endpoint | Method | Purpose | Response |
|----------|--------|---------|----------|
| `/status` | GET | Health check | `{"status": "ok"}` |
| `/history` | GET | Recent analyses | Array of entries |
| `/metrics` | GET | Usage statistics | Metrics object |
| `/favicon.ico` | GET | Favicon | PNG image |

### Example Requests

```bash
# Full Analysis
curl -X POST http://127.0.0.1:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"sql_query": "SELECT * FROM users WHERE id = 1"}'

# Optimize Only
curl -X POST http://127.0.0.1:8000/optimize \
  -H "Content-Type: application/json" \
  -d '{"sql_query": "SELECT * FROM orders"}'

# Health Check
curl http://127.0.0.1:8000/status

# Get History
curl http://127.0.0.1:8000/history?limit=10
```

---

## 📂 File Structure

```
newpro/
├── 📄 main.py                    # FastAPI app (209 lines)
├── 📄 requirements.txt           # Dependencies
├── 📄 .env                       # Environment variables
│
├── 📁 agents/                    # AI Agents
│   ├── base_agent.py            # Base class (21 lines)
│   ├── query_optimizer.py       # Query optimization (194 lines)
│   ├── schema_advisor.py        # Schema analysis (45 lines)
│   ├── data_validator.py        # Validation (46 lines)
│   └── cost_saver.py            # Cost estimation (57 lines)
│
├── 📁 frontend/                  # Web UI
│   ├── index.html               # HTML structure (67 lines)
│   ├── script.js                # JavaScript logic (600+ lines)
│   └── style.css                # Styling (800+ lines)
│
├── 📁 utils/                     # Utilities
│   ├── config.py                # Configuration (55 lines)
│   └── history_store.py         # History storage (75 lines)
│
├── 📁 data/                      # Data storage
│   └── history.jsonl            # Analysis history
│
└── 📁 tests/                     # Test suite
    ├── test_history_store.py
    └── test_split_optimizer.py
```

---

## 🔑 Key Functions

### Backend (Python)

#### main.py

```python
# Main analysis endpoint
@app.post("/analyze")
def analyze_query(request: QueryRequest):
    """Comprehensive query analysis with all agents."""
    pass

# Split optimizer output
def split_optimizer_output(raw_output: str) -> tuple[str, str]:
    """Separates SQL from rationale."""
    pass
```

#### agents/query_optimizer.py

```python
class QueryOptimizer(BaseAgent):
    def optimize_query(self, sql_query: str) -> str:
        """Optimize SQL query using Claude AI."""
        # 1. Detect statement type
        # 2. Build optimization prompt
        # 3. Send to Claude API
        # 4. Return optimized query + rationale
        pass
```

#### agents/data_validator.py

```python
class DataValidator(BaseAgent):
    def validate_query(self, sql_query: str) -> str:
        """Validate syntax, security, and safety."""
        pass
```

#### agents/cost_saver.py

```python
class CostSaver(BaseAgent):
    def save_cost(self, inputs: dict) -> str:
        """Analyze costs and suggest savings."""
        pass
```

#### agents/schema_advisor.py

```python
class SchemaAdvisor(BaseAgent):
    def analyze_schema(self, schema_sql: str) -> str:
        """Analyze schema and suggest improvements."""
        pass
```

#### utils/history_store.py

```python
class HistoryStore:
    def append(self, payload: Dict[str, Any]) -> None:
        """Save analysis to JSONL file."""
        pass
    
    def get_recent(self, limit: int = 20) -> List[Dict]:
        """Get recent analyses."""
        pass
    
    def metrics(self) -> Dict[str, Any]:
        """Get usage statistics."""
        pass
```

### Frontend (JavaScript)

#### script.js

```javascript
// Form submission handler
form.addEventListener("submit", async (e) => {
    // 1. Prevent default
    // 2. Show loading
    // 3. Send POST request
    // 4. Render results
});

// Format SQL with syntax highlighting
const formatSQLBlock = (title, sql) => {
    // Returns HTML with Prism.js code block
};

// Copy to clipboard
const copyToClipboard = async (elementId) => {
    // Uses modern Clipboard API with fallback
};

// Visual comparison diagram
const createQueryComparisonDiagram = (original, optimized) => {
    // Returns HTML with before/after cards
};

// Performance metrics
const createPerformanceMetrics = (text) => {
    // Returns HTML with metric cards
};

// Format text with bullet points
const formatTextBlock = (text) => {
    // Returns HTML with icons and formatting
};
```

---

## ⚙️ Configuration

### Environment Variables

```bash
# Required
CLAUDE_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxxxxxxx

# Optional
CLAUDE_MODEL=claude-3-haiku-20240307  # Default model
API_HOST=127.0.0.1                    # Server host
API_PORT=8000                         # Server port
LOG_LEVEL=INFO                        # Logging level

# Database (for future features)
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASS=password
DB_NAME=testdb
```

### Model Options

| Model | Speed | Cost | Quality | Use Case |
|-------|-------|------|---------|----------|
| `claude-3-haiku-20240307` | ⚡⚡⚡ | 💰 | ⭐⭐⭐ | Default (fast & cheap) |
| `claude-3-sonnet-20240229` | ⚡⚡ | 💰💰 | ⭐⭐⭐⭐ | Better quality |
| `claude-3-opus-20240229` | ⚡ | 💰💰💰 | ⭐⭐⭐⭐⭐ | Best quality |

### Token Limits

```python
# In query_optimizer.py
if statement_type == 'SELECT':
    max_tokens = 1500  # Complex optimizations
elif statement_type in ['CREATE TABLE', 'ALTER TABLE']:
    max_tokens = 1500  # Schema operations
else:
    max_tokens = 1000  # Other operations
```

---

## 💻 Common Commands

### Development

```bash
# Start server with auto-reload
uvicorn main:app --reload

# Start on different port
uvicorn main:app --port 8001

# Start with custom host
uvicorn main:app --host 0.0.0.0

# View logs
uvicorn main:app --log-level debug
```

### Testing

```bash
# Run all tests
pytest

# Run specific test
pytest tests/test_history_store.py

# Run with coverage
pytest --cov=agents --cov=utils

# Run with verbose output
pytest -v -s
```

### Dependency Management

```bash
# Install dependencies
pip install -r requirements.txt

# Update dependencies
pip install --upgrade -r requirements.txt

# Freeze current versions
pip freeze > requirements.txt

# Install single package
pip install anthropic
```

### Virtual Environment

```bash
# Create venv
python3 -m venv venv

# Activate (macOS/Linux)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Deactivate
deactivate

# Remove venv
rm -rf venv
```

### Git Operations

```bash
# Check status
git status

# Add files
git add .

# Commit
git commit -m "Add feature"

# Push
git push origin main

# Pull
git pull origin main
```

---

## 🔧 Troubleshooting

### Issue: "CLAUDE_API_KEY not set"

**Symptoms:**
- Server fails to start
- Error message: "❌ CLAUDE_API_KEY environment variable is not set"

**Solution:**
```bash
# Check if .env exists
ls -la .env

# Add API key
echo "CLAUDE_API_KEY=your_key_here" >> .env

# Verify
cat .env | grep CLAUDE_API_KEY

# Restart server
uvicorn main:app --reload
```

---

### Issue: "Module not found"

**Symptoms:**
- Import errors
- `ModuleNotFoundError: No module named 'fastapi'`

**Solution:**
```bash
# Ensure venv is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt

# Verify installation
pip list | grep fastapi
```

---

### Issue: "Port already in use"

**Symptoms:**
- `OSError: [Errno 48] Address already in use`

**Solution:**
```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>

# Or use different port
uvicorn main:app --port 8001
```

---

### Issue: "Syntax highlighting not working"

**Symptoms:**
- SQL code appears as plain text
- No colors in code blocks

**Solution:**
1. Check browser console for errors
2. Verify Prism.js CDN is accessible
3. Check internet connection
4. Clear browser cache
5. Ensure `Prism.highlightAll()` is called

```javascript
// In script.js, after rendering results
Prism.highlightAll();
```

---

### Issue: "Copy button not working"

**Symptoms:**
- Click does nothing
- Console error: "Clipboard API not available"

**Solution:**
1. **Use HTTPS in production** (Clipboard API requires secure context)
2. Check browser compatibility
3. Verify JavaScript console for errors
4. Fallback method should work in older browsers

```javascript
// Fallback for older browsers
const fallbackCopy = (text) => {
    const textarea = document.createElement('textarea');
    textarea.value = text;
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand('copy');
    document.body.removeChild(textarea);
};
```

---

### Issue: "Slow response times"

**Symptoms:**
- Analysis takes >10 seconds
- Timeout errors

**Solution:**
1. Check Claude API status
2. Reduce token limits
3. Use faster model (Haiku)
4. Check network connection
5. Increase timeout

```python
# In main.py, increase timeout
@app.post("/analyze")
async def analyze_query(request: QueryRequest):
    # Add timeout handling
    pass
```

---

### Issue: "History file growing too large"

**Symptoms:**
- `data/history.jsonl` is several MB
- Slow history queries

**Solution:**
```bash
# Backup current history
cp data/history.jsonl data/history.backup.jsonl

# Keep only last 1000 entries
tail -n 1000 data/history.jsonl > data/history.new.jsonl
mv data/history.new.jsonl data/history.jsonl

# Or rotate logs
mv data/history.jsonl data/history.$(date +%Y%m%d).jsonl
touch data/history.jsonl
```

---

## 📊 Performance Tips

### Optimize Response Time

1. **Use Haiku model** (fastest)
   ```bash
   CLAUDE_MODEL=claude-3-haiku-20240307
   ```

2. **Reduce token limits** (if quality is acceptable)
   ```python
   max_tokens = 800  # Instead of 1500
   ```

3. **Cache common queries** (future enhancement)

4. **Use CDN for frontend assets**

### Reduce API Costs

1. **Use Haiku model** (cheapest)
2. **Reduce max_tokens**
3. **Implement request caching**
4. **Batch similar queries**

### Improve UI Performance

1. **Lazy load Prism.js**
2. **Debounce form submissions**
3. **Use virtual scrolling for long results**
4. **Compress frontend assets**

---

## 🎯 Best Practices

### Code Organization

✅ **DO:**
- Keep functions small and focused
- Use type hints
- Add docstrings
- Follow PEP 8
- Write tests

❌ **DON'T:**
- Hardcode API keys
- Mix concerns
- Ignore errors
- Skip validation
- Commit secrets

### Security

✅ **DO:**
- Use environment variables
- Validate all inputs
- Sanitize outputs
- Use HTTPS in production
- Implement rate limiting

❌ **DON'T:**
- Execute user queries directly
- Trust user input
- Expose API keys
- Skip authentication
- Ignore security warnings

### Performance

✅ **DO:**
- Use async where possible
- Cache common results
- Optimize database queries
- Monitor response times
- Profile bottlenecks

❌ **DON'T:**
- Block event loop
- Make unnecessary API calls
- Load large files synchronously
- Ignore memory leaks
- Skip performance testing

---

## 📚 Quick Links

### Documentation
- [Complete Project Documentation](COMPLETE_PROJECT_DOCUMENTATION.md)
- [Project Flow Diagram](PROJECT_FLOW_DIAGRAM.md)
- [Syntax Highlighting Enhancement](SYNTAX_HIGHLIGHTING_ENHANCEMENT.md)
- [Universal Optimization Fix](UNIVERSAL_OPTIMIZATION_FIX.md)

### External Resources
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Anthropic Claude API](https://docs.anthropic.com/)
- [MariaDB Docs](https://mariadb.com/kb/en/)
- [Prism.js Docs](https://prismjs.com/)

### API Documentation
- Interactive Docs: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
- OpenAPI JSON: http://127.0.0.1:8000/openapi.json

---

## 🎓 Learning Resources

### SQL Optimization
- Window functions in MariaDB
- Correlated subquery optimization
- Index strategies
- Query execution plans

### FastAPI
- Async programming
- Dependency injection
- Request validation
- Error handling

### Frontend
- Modern JavaScript (ES6+)
- Fetch API
- DOM manipulation
- CSS animations

### AI Integration
- Prompt engineering
- Token optimization
- Error handling
- Rate limiting

---

## 📞 Support Checklist

Before asking for help:

- [ ] Check this Quick Reference
- [ ] Review Complete Documentation
- [ ] Check `/status` endpoint
- [ ] Review browser console
- [ ] Check server logs
- [ ] Verify environment variables
- [ ] Test with simple query
- [ ] Check API key validity
- [ ] Verify network connection
- [ ] Try restarting server

---

## 🎉 Quick Wins

### Improve Query Performance
```sql
-- Before (slow)
SELECT (SELECT ...), (SELECT ...)
FROM table;

-- After (fast)
SELECT derived.col1, derived.col2
FROM table
LEFT JOIN (SELECT ... ROW_NUMBER() OVER ...) derived
```

### Add Custom Styling
```css
/* In style.css */
:root {
    --custom-color: #your-color;
}
```

### Change Model
```bash
# In .env
CLAUDE_MODEL=claude-3-sonnet-20240229
```

### Export History
```bash
# Export to JSON
cat data/history.jsonl | jq '.' > history.json

# Export to CSV
cat data/history.jsonl | jq -r '[.timestamp, .type] | @csv' > history.csv
```

---

*Quick Reference Guide - Last Updated: January 2024*
*For detailed information, see [Complete Project Documentation](COMPLETE_PROJECT_DOCUMENTATION.md)*