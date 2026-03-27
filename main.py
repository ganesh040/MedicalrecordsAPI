from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from routers.applications import router as records_router
from routers.auth import router as auth_router
import time
import logging
from database import engine
from models import MedicalRecord
from routers.doctors import router as doctors_router


# ── Logging setup ─────────────────────────
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Medical Records API",
    description="An API to manage patient medical records",
    version="1.0.0",
)

MedicalRecord.metadata.create_all(bind=engine)  # create tables if not exist

# ── Middleware 1 — Log + Response Time ────
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    logger.info(f"→ {request.method} {request.url}")
    
    response = await call_next(request)  # run the actual route
    
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    
    logger.info(f"← {response.status_code} ({process_time:.3f}s)")
    
    return response

# ── Middleware 2 — CORS ───────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # your React frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(records_router)
app.include_router(auth_router)
app.include_router(doctors_router)