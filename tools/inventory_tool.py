import sys, os
sys.path.insert(0, r'P:\supplypulse')
# tools/inventory_tool.py
#
# Reads inventory snapshots and computes risk levels.
# The demand agent uses this to answer:
# "How many weeks of urea do we have?"
# "Which commodities are below the reorder point?"

from db.database import SessionLocal
from db.models import InventorySnapshot


def get_inventory(commodity: str) -> dict | None:
    """
    Returns the latest inventory snapshot for a commodity.
    
    Returns a dict with stock level, weeks remaining,
    reorder point, and a computed risk_level field.
    """
    db = SessionLocal()
    try:
        snapshot = (
            db.query(InventorySnapshot)
            .filter(InventorySnapshot.commodity == commodity.lower())
            .order_by(InventorySnapshot.snapshot_date.desc())  # Most recent
            .first()
        )
        if not snapshot:
            return None
        
        result = {
            "commodity": snapshot.commodity,
            "quantity_available": snapshot.quantity_available,
            "unit": snapshot.unit,
            "weeks_of_stock": snapshot.weeks_of_stock,
            "reorder_point": snapshot.reorder_point,
            "snapshot_date": str(snapshot.snapshot_date),
            # Compute risk level right here so the agent gets a clear signal
            "risk_level": _compute_risk(snapshot.weeks_of_stock, snapshot.reorder_point, snapshot.quantity_available)
        }
        return result
    finally:
        db.close()


def get_all_inventory() -> list[dict]:
    """Returns the latest snapshot for every commodity — used by the orchestrator
    for a full system health check."""
    db = SessionLocal()
    try:
        # Get distinct commodities first, then latest of each
        commodities = db.query(InventorySnapshot.commodity).distinct().all()
        results = []
        for (commodity,) in commodities:
            snapshot = (
                db.query(InventorySnapshot)
                .filter(InventorySnapshot.commodity == commodity)
                .order_by(InventorySnapshot.snapshot_date.desc())
                .first()
            )
            if snapshot:
                results.append({
                    "commodity": snapshot.commodity,
                    "quantity_available": snapshot.quantity_available,
                    "unit": snapshot.unit,
                    "weeks_of_stock": snapshot.weeks_of_stock,
                    "reorder_point": snapshot.reorder_point,
                    "risk_level": _compute_risk(
                        snapshot.weeks_of_stock,
                        snapshot.reorder_point,
                        snapshot.quantity_available
                    )
                })
        return results
    finally:
        db.close()


def get_critical_commodities() -> list[dict]:
    """
    Returns only the commodities that are below their reorder point.
    This is the key function for the demo — it immediately highlights
    what needs urgent action.
    """
    all_inventory = get_all_inventory()
    return [
        item for item in all_inventory
        if item["quantity_available"] < item["reorder_point"]
    ]


def _compute_risk(weeks_of_stock: float, reorder_point: float, quantity: float) -> str:
    """
    Translates raw numbers into a human-readable risk level.
    
    Logic mirrors how real procurement managers think:
    - Under 2 weeks = critical (you WILL run out before new stock arrives)
    - Under 4 weeks = high (you need to order NOW)
    - Under 6 weeks = medium (monitor closely)
    - Above 6 weeks = low
    """
    if weeks_of_stock < 2:
        return "critical"
    elif weeks_of_stock < 4:
        return "high"
    elif weeks_of_stock < 6:
        return "medium"
    else:
        return "low"


# ── Quick test ──────────────────────────────────────────────────────────────
# python -m tools.inventory_tool
if __name__ == "__main__":
    print("=== Full inventory status ===")
    for item in get_all_inventory():
        print(f"  {item['commodity']:10} | {item['weeks_of_stock']} weeks | risk: {item['risk_level'].upper()}")
    
    print("\n=== Critical commodities (below reorder point) ===")
    critical = get_critical_commodities()
    if critical:
        for item in critical:
            print(f"  !! {item['commodity']} — only {item['quantity_available']:,} {item['unit']} left")
    else:
        print("  None — all commodities above reorder point")