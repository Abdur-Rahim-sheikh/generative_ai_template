from arq.connections import ArqRedis
from fastapi import Request


def get_job_queue(request: Request) -> ArqRedis:
    return request.app.state.arq_pool
