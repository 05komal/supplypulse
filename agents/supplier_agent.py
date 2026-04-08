async def run(query: str):
    q = query.lower()

    suppliers = []
    risk_score = 0
    notes = []

    # --- Detect disruption context ---
    if "saudi" in q or "middle east" in q:
        suppliers.append("Oman Fertilizer Company")
        suppliers.append("Qatar Chemical Co.")
        risk_score += 30
        notes.append("Primary Middle East supplier disruption")

    if "china" in q:
        suppliers.append("Vietnam Agro Supplies")
        suppliers.append("Indonesia Fertilizer Corp")
        risk_score += 25
        notes.append("China supply restriction")

    if "port" in q or "delay" in q:
        suppliers.append("Domestic backup suppliers (Gujarat, Maharashtra)")
        risk_score += 20
        notes.append("Logistics disruption affecting imports")

    # --- Default fallback ---
    if not suppliers:
        suppliers = [
            "Domestic suppliers (IFFCO, KRIBHCO)",
            "Regional distributors"
        ]
        notes.append("No major supplier disruption detected")

    # --- Risk level ---
    if risk_score >= 60:
        level = "HIGH"
        action = "Immediately switch to alternate international suppliers and increase domestic procurement."
    elif risk_score >= 30:
        level = "MEDIUM"
        action = "Diversify supplier base and monitor shipment timelines."
    else:
        level = "LOW"
        action = "Continue with existing suppliers, maintain buffer stock."

    # --- Output ---
    return f"""Supplier Risk Level: {level}

Alternative Suppliers:
- {'; '.join(suppliers)}

Key Notes:
- {'; '.join(notes)}

Recommended Action:
{action}"""