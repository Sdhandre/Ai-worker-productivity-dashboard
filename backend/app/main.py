from fastapi import FastAPI
from .database import Base, engine
from . import models
from .routes import seed,events, metrics
from fastapi.middleware.cors import CORSMiddleware

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


@app.get("/")
def health():
    return {"status": "ok"}
