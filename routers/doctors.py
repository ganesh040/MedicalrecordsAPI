from fastapi import APIRouter, Depends, HTTPException, status, Path
from typing import Annotated
from sqlalchemy.orm import Session,selectinload
from database import get_db
from models import Doctor
from pydantic import BaseModel, Field, EmailStr
from routers.auth import get_current_user


# ── Schemas ───────────────────────────────
class DoctorIn(BaseModel):
    name:           str      = Field(min_length=2, max_length=100)
    email:          EmailStr
    specialization: str      = Field(min_length=2, max_length=100)
    phone:          str | None = None


class DoctorOut(BaseModel):
    id:             int
    name:           str
    email:          str
    specialization: str
    phone:          str | None
    records:       list=[]  # ← new field for related medical records

    model_config = {"from_attributes": True}

router = APIRouter(
    prefix="/doctors",
    tags=["Doctors"],
)

# ── POST /doctors/ ────────────────────────
@router.post(
    "/",
    response_model=DoctorOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new doctor",
)
async def create_doctor(
    _: Annotated[dict, Depends(get_current_user)],
    doctor: DoctorIn,
    db: Annotated[Session, Depends(get_db)]
):
    db_doctor = Doctor(**doctor.model_dump())
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor


# ── GET /doctors/ ─────────────────────────
@router.get(
    "/",
    response_model=list[DoctorOut],
    summary="Get all doctors",
)
async def get_doctors(
    _: Annotated[dict, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)]
):
    return db.query(Doctor).all()


# ── GET /doctors/{id} ─────────────────────
@router.get(
    "/{doctor_id}",
    response_model=DoctorOut,
    summary="Get a doctor by ID",
)
async def get_doctor(
    _: Annotated[dict, Depends(get_current_user)],
    doctor_id: Annotated[int, Path(ge=1)],
    db: Annotated[Session, Depends(get_db)]
):
    doctor = db.query(Doctor).options(selectinload(Doctor.records)).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor not found"
        )
    return doctor


# ── DELETE /doctors/{id} ──────────────────
@router.delete(
    "/{doctor_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a doctor",
)
async def delete_doctor(
    _: Annotated[dict, Depends(get_current_user)],
    doctor_id: Annotated[int, Path(ge=1)],
    db: Annotated[Session, Depends(get_db)]
):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor not found"
        )
    db.delete(doctor)
    db.commit()