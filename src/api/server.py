import logging
import time

from fastapi import FastAPI, Request

from src.api.routes import router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ztsi.api")

app = FastAPI(
    title="ZT&SI Stability Gateway",
    description="ZT&SI Stability Gateway — Cognitive Runtime Firewall",
    version="0.2.0",
)


@app.middleware("http")
async def timing_logger(request: Request, call_next):
    started_at = time.perf_counter()
    response = await call_next(request)
    duration_ms = (time.perf_counter() - started_at) * 1000
    response.headers["X-ZTSI-Process-Time-Ms"] = f"{duration_ms:.3f}"
    logger.info(
        "method=%s path=%s status=%s duration_ms=%.3f",
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
    )
    return response


app.include_router(router)
