from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.services.job_engine import shortlist_candidates

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():

    return {
        "status": "running"
    }


@app.get("/shortlist")
def shortlist():

    return shortlist_candidates()