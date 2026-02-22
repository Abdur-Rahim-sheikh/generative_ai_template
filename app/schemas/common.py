from pydantic import BaseModel


class JobResponse(BaseModel):
    job_id: str


class StatusResponse(BaseModel):
    status: str
    message: str
    results: list[str] | None = None
