# test_client.py
import requests, json

API = "http://127.0.0.1:8000/analyze"
sql = """
SELECT * FROM your_table LIMIT 5;
"""

payload = {
    "sql": sql,
    "tables": [],
    "run_in_sandbox": True
}

r = requests.post(API, json=payload, timeout=120)
print("Status:", r.status_code)
print(json.dumps(r.json(), indent=2, default=str))