from agents.disruption_agent import run as disruption
from agents.supplier_agent import run as supplier
from agents.demand_agent import run as demand
from agents.finance_agent import run as finance
import uuid
import time

async def run_supply_pulse(query: str):
    start = time.time()

    d = await disruption(query)
    s = await supplier(query)
    dm = await demand(query)
    f = await finance(query)

    duration = int((time.time() - start) * 1000)

    return {
        "query_id": str(uuid.uuid4()),
        "query": query,
        "duration_ms": duration,
        "agent_outputs": {
            "disruption": d,
            "supplier": s,
            "demand": dm,
            "finance": f
        },
        "final_report": f"""
FINAL REPORT:

[DISRUPTION ANALYSIS]
{d}

[SUPPLIER ANALYSIS]
{s}

[DEMAND ANALYSIS]
{dm}

[FINANCE ANALYSIS]
{f}
"""}