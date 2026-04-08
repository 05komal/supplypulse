async def run(query: str):
    q = query.lower()

    demand_score = 0
    factors = []

    # --- Seasonal demand ---
    if "rabi" in q or "winter" in q:
        demand_score += 30
        factors.append("Seasonal agricultural demand increase")

    if "kharif" in q or "monsoon" in q:
        demand_score += 25
        factors.append("Monsoon-driven demand")

    # --- Demand spikes ---
    if "increase" in q or "spike" in q or "high demand" in q:
        demand_score += 20
        factors.append("Sudden demand surge")

    # --- Low supply effect ---
    if "shortage" in q:
        demand_score += 15
        factors.append("Market shortage driving demand pressure")

    # --- Normalize ---
    demand_score = min(demand_score, 100)

    # --- Demand level ---
    if demand_score >= 60:
        level = "HIGH"
        insight = "Demand will significantly exceed supply."
    elif demand_score >= 30:
        level = "MEDIUM"
        insight = "Demand expected to rise moderately."
    else:
        level = "LOW"
        insight = "Stable demand conditions."

    return f"""Demand Score: {demand_score}/100
Demand Level: {level}

Key Drivers:
- {'; '.join(factors) if factors else 'No major demand signals'}

Insight:
{insight}"""