from fastapi import APIRouter
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from ..database import SessionLocal
from ..models import Worker, Workstation,Event

router = APIRouter(prefix="/seed", tags=["Seed"])

@router.post("")
def seed_workers_and_stations():
    db: Session = SessionLocal()

    # 1. Clear existing data (order matters due to FK)
    db.query(Event).delete()
    db.query(Worker).delete()
    db.query(Workstation).delete()
    db.commit()

    # 2. Create workers
    workers = [
        Worker(worker_id="W1", name="Worker 1"),
        Worker(worker_id="W2", name="Worker 2"),
        Worker(worker_id="W3", name="Worker 3"),
        Worker(worker_id="W4", name="Worker 4"),
        Worker(worker_id="W5", name="Worker 5"),
        Worker(worker_id="W6", name="Worker 6"),
    ]

    # 3. Create workstations
    stations = [
        Workstation(station_id="S1", name="Station 1"),
        Workstation(station_id="S2", name="Station 2"),
        Workstation(station_id="S3", name="Station 3"),
        Workstation(station_id="S4", name="Station 4"),
        Workstation(station_id="S5", name="Station 5"),
        Workstation(station_id="S6", name="Station 6"),
    ]

    db.add_all(workers + stations)
    db.commit()

    # 4. Create DEMO EVENTS (this is what fixes zero metrics)
    now = datetime.utcnow()

    demo_events = [
        # W1 – balanced
        Event(timestamp=now - timedelta(minutes=60), worker_id="W1", workstation_id="S1", event_type="working"),
        Event(timestamp=now - timedelta(minutes=40), worker_id="W1", workstation_id="S1", event_type="idle"),
        Event(timestamp=now - timedelta(minutes=30), worker_id="W1", workstation_id="S1", event_type="working"),
        Event(timestamp=now - timedelta(minutes=10), worker_id="W1", workstation_id="S1", event_type="product_count", count=5),

        # W2 – high performer
        Event(timestamp=now - timedelta(minutes=60), worker_id="W2", workstation_id="S2", event_type="working"),
        Event(timestamp=now - timedelta(minutes=30), worker_id="W2", workstation_id="S2", event_type="product_count", count=3),
        Event(timestamp=now - timedelta(minutes=10), worker_id="W2", workstation_id="S2", event_type="product_count", count=4),

        # W3 – late start
        Event(timestamp=now - timedelta(minutes=60), worker_id="W3", workstation_id="S3", event_type="idle"),
        Event(timestamp=now - timedelta(minutes=35), worker_id="W3", workstation_id="S3", event_type="working"),
        Event(timestamp=now - timedelta(minutes=15), worker_id="W3", workstation_id="S3", event_type="product_count", count=2),

        # W4 – mostly idle
        Event(timestamp=now - timedelta(minutes=60), worker_id="W4", workstation_id="S4", event_type="idle"),

        # W5 – absent
        Event(timestamp=now - timedelta(minutes=60), worker_id="W5", workstation_id="S5", event_type="absent"),

        # W6 – mixed
        Event(timestamp=now - timedelta(minutes=60), worker_id="W6", workstation_id="S6", event_type="working"),
        Event(timestamp=now - timedelta(minutes=45), worker_id="W6", workstation_id="S6", event_type="idle"),
        Event(timestamp=now - timedelta(minutes=25), worker_id="W6", workstation_id="S6", event_type="working"),
        Event(timestamp=now - timedelta(minutes=5), worker_id="W6", workstation_id="S6", event_type="product_count", count=1),
    ]

    db.add_all(demo_events)
    db.commit()
    db.close()

    return {
        "status": "seeded",
        "workers": 6,
        "stations": 6,
        "events": len(demo_events),
    }
