from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from routers.applications import router as records_router
from routers.auth import router as auth_router
from routers.doctors import router as doctors_router
from database import engine
from models import Base
from config import get_settings
import time
import logging

settings = get_settings()

# ── Logging setup ─────────────────────────
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
)

Base.metadata.create_all(bind=engine)

# ── Middleware 1 — Log + Response Time ────
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    logger.info(f"→ {request.method} {request.url}")
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    logger.info(f"← {response.status_code} ({process_time:.3f}s)")
    return response

# ── Middleware 2 — CORS ───────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(records_router)
app.include_router(auth_router)
app.include_router(doctors_router)

@app.get("/", tags=["Health"])
async def root():
    return {
        "api":     settings.app_name,
        "version": settings.app_version,
        "status":  "running",
        "docs":    "/docs"
    }

@app.get("/health", tags=["Health"])
async def health():
    return {"status": "ok"}