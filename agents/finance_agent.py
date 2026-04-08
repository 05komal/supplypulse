async def run(query: str):
    q = query.lower()

    cost_impact = 0
    factors = []

    # --- Price increase ---
    if "price" in q or "increase" in q:
        cost_impact += 30
        factors.append("Rising procurement cost")

    # --- Logistics disruption ---
    if "delay" in q or "port" in q:
        cost_impact += 20
        factors.append("Logistics and holding cost increase")

    # --- Supply shortage ---
    if "shortage" in q:
        cost_impact += 25
        factors.append("Scarcity-driven price surge")

    # --- High demand ---
    if "demand" in q or "season" in q:
        cost_impact += 15
        factors.append("Demand pressure increasing cost")

    # --- Normalize ---
    cost_impact = min(cost_impact, 100)

    # --- Impact level ---
    if cost_impact >= 60:
        level = "HIGH"
        insight = "Significant cost escalation expected."
    elif cost_impact >= 30:
        level = "MEDIUM"
        insight = "Moderate cost increase likely."
    else:
        level = "LOW"
        insight = "Minimal financial impact."

    return f"""Cost Impact Score: {cost_impact}/100
Impact Level: {level}

Cost Drivers:
- {'; '.join(factors) if factors else 'No major cost drivers'}

Financial Insight:
{insight}"""