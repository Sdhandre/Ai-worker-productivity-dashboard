from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey,String
from .database import Base
from datetime import datetime

class Worker(Base):
    __tablename__ = "workers"
    worker_id = Column(String, primary_key=True)
    name = Column(String)

class Workstation(Base):
    __tablename__ = "workstations"
    station_id = Column(String, primary_key=True)
    name = Column(String)

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, nullable=False)
    worker_id = Column(String, ForeignKey("workers.worker_id"), nullable=False)
    workstation_id = Column(String, ForeignKey("workstations.station_id"), nullable=False)
    event_type = Column(String, nullable=False)
    confidence = Column(Float)
    count = Column(Integer)