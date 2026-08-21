from __future__ import annotations

from fastapi import BackgroundTasks, FastAPI, HTTPException
from pydantic import BaseModel
from uuid import uuid4

from pipeline import run_bioquery


app = FastAPI(
    title="BioQuery API",
    description="AI-assisted biological investigation workflow",
    version="0.1.0",
)


class InvestigationRequest(BaseModel):
    topic: str
    question: str
    existing_knowledge: str
    depth: str
    gene: str
    organism_id: int

jobs: dict[str, dict] = {}


@app.get("/health")
def health_check() -> dict:
    return {
        "status": "ok",
        "service": "BioQuery",
    }

def run_investigation_job(
    job_id: str,
    request: InvestigationRequest,
) -> None:
    """Run a BioQuery investigation and store its result."""

    try:
        result = run_bioquery(
            topic=request.topic,
            question=request.question,
            existing_knowledge=request.existing_knowledge,
            depth=request.depth,
            gene=request.gene,
            organism_id=request.organism_id,
        )

        jobs[job_id] = {
            "status": "completed",
            "result": result,
        }

    except Exception as error:
        jobs[job_id] = {
            "status": "failed",
            "error": str(error),
        }



@app.post("/investigate")
def investigate(
    request: InvestigationRequest,
    background_tasks: BackgroundTasks,
) -> dict:
    job_id = str(uuid4())

    jobs[job_id] = {
        "status": "running",
    }

    background_tasks.add_task(
        run_investigation_job,
        job_id,
        request,
    )

    return {
        "job_id": job_id,
        "status": "running",
    }

@app.get("/results/{job_id}")
def get_result(job_id: str) -> dict:
    job = jobs.get(job_id)

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found.",
        )

    return job