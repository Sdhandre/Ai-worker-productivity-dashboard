from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from ..database import SessionLocal
from ..models import Event

router = APIRouter(prefix="/events", tags=["Events"])

@router.post("")
def ingest_event(event: dict):
    db: Session = SessionLocal()

    try:
        db_event = Event(
            timestamp=datetime.fromisoformat(
                event["timestamp"].replace("Z", "")
            ),
            worker_id=event["worker_id"],
            workstation_id=event["workstation_id"],
            event_type=event["event_type"],
            confidence=event.get("confidence"),
            count=event.get("count")
        )
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Missing field: {e}")

    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    db.close()

    return {"status": "stored", "event_id": db_event.id}
