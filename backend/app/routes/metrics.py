from fastapi import APIRouter
from sqlalchemy.orm import Session
from collections import defaultdict

from ..database import SessionLocal
from ..models import Event, Worker,Workstation
from ..metrics import compute_worker_metrics,compute_workstation_metrics

router = APIRouter(prefix="/metrics", tags=["Metrics"])

@router.get("/workers")
def get_worker_metrics():
    db: Session = SessionLocal()

    # Fetch all workers
    workers = db.query(Worker).all()

    # Fetch all events, ordered by time
    events = db.query(Event).order_by(Event.timestamp).all()

    # Group events by worker_id
    events_by_worker = defaultdict(list)
    for event in events:
        events_by_worker[event.worker_id].append(event)

    response = []

    for worker in workers:
        worker_events = events_by_worker.get(worker.worker_id, [])

        metrics = compute_worker_metrics(worker_events)

        response.append({
            "worker_id": worker.worker_id,
            "name": worker.name,
            **metrics
        })

    db.close()
    return response

@router.get("/workstations")
def get_workstation_metrics():
    db: Session = SessionLocal()

    workstations = db.query(Workstation).all()
    events = db.query(Event).order_by(Event.timestamp).all()

    from collections import defaultdict
    events_by_station = defaultdict(list)

    for event in events:
        events_by_station[event.workstation_id].append(event)

    response = []

    for station in workstations:
        station_events = events_by_station.get(station.station_id, [])

        metrics = compute_workstation_metrics(station_events)

        response.append({
            "station_id": station.station_id,
            "name": station.name,
            **metrics
        })

    db.close()
    return response

@router.get("/factory")
def get_factory_metrics():
    db: Session = SessionLocal()

    workers = db.query(Worker).all()
    events = db.query(Event).order_by(Event.timestamp).all()

    from collections import defaultdict
    events_by_worker = defaultdict(list)

    for event in events:
        events_by_worker[event.worker_id].append(event)

    total_working_time = 0
    total_units = 0
    utilization_values = []

    for worker in workers:
        worker_events = events_by_worker.get(worker.worker_id, [])
        metrics = compute_worker_metrics(worker_events)

        total_working_time += metrics["working_time_sec"]
        total_units += metrics["total_units"]

        if (metrics["working_time_sec"] + metrics["idle_time_sec"]) > 0:
            utilization_values.append(metrics["utilization"])

    average_utilization = (
        sum(utilization_values) / len(utilization_values)
        if utilization_values else 0
    )

    avg_production_rate = 0
    if total_working_time > 0:
        avg_production_rate = total_units / (total_working_time / 3600)

    db.close()

    return {
        "total_productive_time_sec": total_working_time,
        "total_units_produced": total_units,
        "average_utilization": average_utilization,
        "average_production_rate_units_per_hour": avg_production_rate
    }
