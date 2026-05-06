from contextlib import asynccontextmanager

from arq import create_pool
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from .config import app_logger, settings
from .entrypoints.api.admin_portal import router as adminRouter
from .entrypoints.api.diffusion_api import router as diffusionRouter
from .entrypoints.api.llm_api import router as llmRouter
from .entrypoints.workers import REDIS_SETTINGS
from .database import init_db, drop_db


@asynccontextmanager
async def lifespan(_app: FastAPI):
    _app.state.arq_pool = await create_pool(settings_=REDIS_SETTINGS)
    app_logger.info("Redis pool created")
    await init_db()
    app_logger.info("Database initialized")
    yield
    await _app.state.arq_pool.close()
    app_logger.info("Redis pool closed")
    await drop_db()
    app_logger.info("Database dropped")


app = FastAPI(
    title="Generative AI Template",
    summary="The Template of AI backbone",
    openapi_url="/openapi.json" if settings.DEBUG else None,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    lifespan=lifespan,
)

app.include_router(llmRouter, prefix="/api/llm", tags=["llm"])
app.include_router(diffusionRouter, prefix="/api/diffusion", tags=["diffusion"])
if settings.DEBUG:
    app.include_router(adminRouter, prefix="/admin", tags=["Admin"])


@app.get("/healthcheck")
def healthcheck():
    return JSONResponse(content="OK!")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
