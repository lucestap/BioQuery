from __future__ import annotations

from uuid import uuid4

from fastapi import BackgroundTasks, FastAPI, HTTPException
from pydantic import BaseModel

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

# V1 keeps job state in memory for lightweight local/Make.com orchestration.
# A production deployment would replace this with persistent job storage.

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
    """Execute a long-running investigation and update its job state.

    Background execution prevents automation clients such as Make.com from
    holding a single HTTP connection open for the full investigation.
    """

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
    """Start an asynchronous BioQuery investigation and return its job ID."""
    job_id = str(uuid4())

    jobs[job_id] = {
        "status": "running",
    }

    # Return control to the caller immediately while BioQuery continues in
    # the background; Make.com can retrieve the result using the job ID.
    
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
    """Return the current state or completed result for an investigation."""
    job = jobs.get(job_id)

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found.",
        )

    return job