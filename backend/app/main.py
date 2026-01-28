from fastapi import FastAPI
from .database import Base, engine
from . import models
from .routes import seed,events, metrics
from fastapi.middleware.cors import CORSMiddleware
from .routes.seed import seed_workers_and_stations
from .database import SessionLocal
from .models import Event

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(seed.router)  
app.include_router(events.router) 
app.include_router(metrics.router)


@app.on_event("startup")
def auto_seed_if_empty():
    db = SessionLocal()
    has_events = db.query(Event).first()
    db.close()

    if not has_events:
        seed_workers_and_stations()


@app.get("/")
def health():
    return {"status": "ok"}
