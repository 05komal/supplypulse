from db.database import SessionLocal, engine
from db.models import Base, Supplier, InventorySnapshot, SupplyEvent

def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    db.query(Supplier).delete()
    db.query(InventorySnapshot).delete()
    db.query(SupplyEvent).delete()

    suppliers = [
        Supplier(name="SABIC Agri-Nutrients", country="Saudi Arabia",
                 commodity="urea", lead_time_days=18, reliability_score=0.92,
                 price_per_unit=310.0, unit="MT", contact_info={"email": "supply@sabic.com"}),
        Supplier(name="OCI Nitrogen", country="Oman",
                 commodity="urea", lead_time_days=14, reliability_score=0.88,
                 price_per_unit=295.0, unit="MT", contact_info={"email": "trade@oci.com"}),
        Supplier(name="Yuzhne Port Agro", country="Ukraine",
                 commodity="urea", lead_time_days=28, reliability_score=0.61,
                 price_per_unit=270.0, unit="MT", contact_info={"email": "export@yuzhne.ua"}),
        Supplier(name="Nutrien Ltd", country="Canada",
                 commodity="potash", lead_time_days=32, reliability_score=0.95,
                 price_per_unit=480.0, unit="MT", contact_info={"email": "india@nutrien.com"}),
        Supplier(name="Belaruskali", country="Belarus",
                 commodity="potash", lead_time_days=35, reliability_score=0.55,
                 price_per_unit=420.0, unit="MT", contact_info={"email": "trade@bkali.by"}),
        Supplier(name="Qatar Energy LNG", country="Qatar",
                 commodity="LNG", lead_time_days=10, reliability_score=0.93,
                 price_per_unit=14.2, unit="MMBTU", contact_info={"email": "lng@qatarenergy.qa"}),
        Supplier(name="GAIL India", country="India",
                 commodity="LNG", lead_time_days=3, reliability_score=0.97,
                 price_per_unit=12.5, unit="MMBTU", contact_info={"email": "commercial@gail.co.in"}),
    ]

    inventory = [
        InventorySnapshot(commodity="urea", quantity_available=180000,
                          unit="MT", weeks_of_stock=3.2, reorder_point=200000),
        InventorySnapshot(commodity="potash", quantity_available=42000,
                          unit="MT", weeks_of_stock=5.8, reorder_point=50000),
        InventorySnapshot(commodity="LNG", quantity_available=95000,
                          unit="MMBTU", weeks_of_stock=2.1, reorder_point=100000),
    ]

    events = [
        SupplyEvent(event_type="port_congestion", location="Kandla Port, Gujarat",
                    severity="high",
                    description="Severe congestion at Kandla port. Delays of 8-12 days for bulk cargo.",
                    affected_commodities=["urea", "potash"],
                    source_url="https://example.com/kandla"),
        SupplyEvent(event_type="geo_risk", location="Strait of Hormuz",
                    severity="critical",
                    description="Increased maritime risk. LNG carriers rerouting via Cape of Good Hope.",
                    affected_commodities=["LNG", "urea"],
                    source_url="https://example.com/hormuz"),
    ]

    db.add_all(suppliers)
    db.add_all(inventory)
    db.add_all(events)
    db.commit()
    db.close()
    print("Database seeded successfully.")

if __name__ == "__main__":
    seed()