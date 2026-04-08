async def run(query: str):
    q = query.lower()

    risk_score = 0
    reasons = []

    # --- Detect disruption keywords ---
    if "delay" in q or "disrupt" in q or "closure" in q:
        risk_score += 30
        reasons.append("Logistics disruption detected")

    if "port" in q or "shipping" in q:
        risk_score += 20
        reasons.append("Port/shipping issue")

    # --- Inventory risk ---
    if "2 weeks" in q or "low stock" in q:
        risk_score += 25
        reasons.append("Low inventory buffer")

    if "demand" in q or "winter" in q or "season" in q:
        risk_score += 15
        reasons.append("Demand surge expected")

    # --- Cap score ---
    risk_score = min(risk_score, 100)

    # --- Risk level ---
    if risk_score >= 70:
        level = "HIGH"
        action = "Immediate mitigation required: activate alternate suppliers and increase buffer stock."
    elif risk_score >= 40:
        level = "MEDIUM"
        action = "Monitor closely and prepare contingency plans."
    else:
        level = "LOW"
        action = "No immediate action required."

    # --- Format clean output (UI friendly) ---
    return f"""Risk Score: {risk_score}/100
Risk Level: {level}

Key Issues:
- {'; '.join(reasons) if reasons else 'No major risks detected'}

Recommended Action:
{action}"""