import sys, os
sys.path.insert(0, r'P:\supplypulse')
# tools/supplier_tool.py
#
# Queries the supplier registry in PostgreSQL.
# The supplier agent calls these functions to answer questions like:
# "Who can supply urea as an alternative to Saudi Arabia?"
# "What's the average lead time for potash suppliers?"

from db.database import SessionLocal
from db.models import Supplier


def get_suppliers_by_commodity(commodity: str) -> list[dict]:
    """
    Returns all active suppliers for a given commodity,
    sorted by reliability score (best first).
    
    Args:
        commodity: e.g. "urea", "potash", "LNG"
    
    Returns:
        List of supplier dicts with all key fields.
    """
    db = SessionLocal()
    try:
        suppliers = (
            db.query(Supplier)
            .filter(
                Supplier.commodity == commodity.lower(),
                Supplier.is_active == 1
            )
            .order_by(Supplier.reliability_score.desc())
            .all()
        )
        
        # Convert SQLAlchemy objects to plain dicts — agents work with dicts, not ORM objects
        return [_supplier_to_dict(s) for s in suppliers]
    
    finally:
        db.close()   # Always close — prevents connection pool exhaustion


def get_supplier_by_country(commodity: str, country: str) -> dict | None:
    """
    Finds a specific supplier by commodity + country.
    Useful when the agent needs to check if a specific
    country's supplier is available as an alternative.
    """
    db = SessionLocal()
    try:
        supplier = (
            db.query(Supplier)
            .filter(
                Supplier.commodity == commodity.lower(),
                Supplier.country == country,
                Supplier.is_active == 1
            )
            .first()
        )
        return _supplier_to_dict(supplier) if supplier else None
    finally:
        db.close()


def get_fastest_suppliers(commodity: str, max_lead_time_days: int = 20) -> list[dict]:
    """
    Returns suppliers who can deliver within a given lead time.
    Critical for the demo scenario — when stock is low, you need
    suppliers who can deliver fast, not just cheaply.
    
    Args:
        commodity: The material needed
        max_lead_time_days: Only return suppliers faster than this
    """
    db = SessionLocal()
    try:
        suppliers = (
            db.query(Supplier)
            .filter(
                Supplier.commodity == commodity.lower(),
                Supplier.lead_time_days <= max_lead_time_days,
                Supplier.is_active == 1
            )
            .order_by(Supplier.lead_time_days.asc())   # Fastest first
            .all()
        )
        return [_supplier_to_dict(s) for s in suppliers]
    finally:
        db.close()


def get_all_commodities() -> list[str]:
    """Returns the distinct list of commodities in the supplier registry."""
    db = SessionLocal()
    try:
        results = db.query(Supplier.commodity).distinct().all()
        return [r[0] for r in results]
    finally:
        db.close()


def _supplier_to_dict(supplier: Supplier) -> dict:
    """Converts a Supplier ORM object to a plain dict."""
    return {
        "id": supplier.id,
        "name": supplier.name,
        "country": supplier.country,
        "commodity": supplier.commodity,
        "lead_time_days": supplier.lead_time_days,
        "reliability_score": supplier.reliability_score,
        "price_per_unit": supplier.price_per_unit,
        "unit": supplier.unit,
        "contact_info": supplier.contact_info
    }


# ── Quick test ──────────────────────────────────────────────────────────────
# python -m tools.supplier_tool
if __name__ == "__main__":
    print("=== Urea suppliers (best reliability first) ===")
    for s in get_suppliers_by_commodity("urea"):
        print(f"  {s['name']} | {s['country']} | {s['lead_time_days']}d | score: {s['reliability_score']}")

    print("\n=== Fast urea suppliers (≤20 days) ===")
    for s in get_fastest_suppliers("urea", max_lead_time_days=20):
        print(f"  {s['name']} | {s['lead_time_days']} days | ₹{s['price_per_unit']}/{s['unit']}")

    print("\n=== All commodities in registry ===")
    print(" ", get_all_commodities())