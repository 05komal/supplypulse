from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import FileResponse

app = FastAPI()


class QueryRequest(BaseModel):
    query: str


@app.get("/")
def home():
    return FileResponse("api/index.html")


@app.post("/query")
async def run_query(request: QueryRequest):
    try:
        from agents.orchestrator import run_supply_pulse
        result = await run_supply_pulse(request.query)
        return result   # ✅ return dict directly
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {
            "query_id": "error",
            "query": request.query,
            "duration_ms": 0,
            "agent_outputs": {
                "disruption": "Error",
                "supplier": "Error",
                "demand": "Error",
                "finance": "Error"
            },
            "final_report": f"Error: {str(e)}"
        }