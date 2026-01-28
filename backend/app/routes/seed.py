from fastapi import APIRouter
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import Worker, Workstation

router = APIRouter(prefix="/seed", tags=["Seed"])

@router.post("")
def seed_workers_and_stations():
    db: Session = SessionLocal()

    # Clear existing data (important for repeatability)
    db.query(Worker).delete()
    db.query(Workstation).delete()

    workers = [
        Worker(worker_id="W1", name="Worker 1"),
        Worker(worker_id="W2", name="Worker 2"),
        Worker(worker_id="W3", name="Worker 3"),
        Worker(worker_id="W4", name="Worker 4"),
        Worker(worker_id="W5", name="Worker 5"),
        Worker(worker_id="W6", name="Worker 6"),
    ]

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
    db.close()

    return {"status": "seeded", "workers": 6, "stations": 6}
