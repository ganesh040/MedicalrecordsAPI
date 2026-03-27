from fastapi import APIRouter, Depends, HTTPException, Query, status, Path, Header
from fastapi.encoders import jsonable_encoder
from typing import Annotated
from sqlalchemy.orm import Session
from schemas.records import MedicalRecord, Bloodtype, RecordFilter
from database import get_db
from models import MedicalRecord as MedicalRecordDB
from routers.auth import get_current_user

router = APIRouter(
    prefix="/records",
    tags=["Medical Records"],
)

# ── Dependency — get record or 404 ────────
def get_record_or_404(
    record_id: Annotated[int, Path(ge=1)],
    db: Annotated[Session, Depends(get_db)]
) -> MedicalRecordDB:
    record = db.query(MedicalRecordDB).filter(MedicalRecordDB.id == record_id).first()
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Record not found"
        )
    return record


# ── POST /records/ ────────────────────────
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new medical record",
    response_description="The newly created record",
)
async def create_record(
    _: Annotated[dict, Depends(get_current_user)],
    record: MedicalRecord,
    db: Annotated[Session, Depends(get_db)]
):
    # convert Pydantic model to dict
    data = jsonable_encoder(record)

    # create SQLAlchemy model from dict
    db_record = MedicalRecordDB(**data)

    # store in PostgreSQL
    db.add(db_record)
    db.commit()
    db.refresh(db_record)  # get updated data back (id, created_at etc)
    return db_record


# ── GET /records/ ─────────────────────────
@router.get(
    "/",
    summary="Get all medical records",
)
async def get_records(
    _: Annotated[dict, Depends(get_current_user)],
    filters: Annotated[RecordFilter, Query()],
    db: Annotated[Session, Depends(get_db)]
):
    query = db.query(MedicalRecordDB)

    # apply filters
    if filters.doctor:
        query = query.filter(MedicalRecordDB.doctor == filters.doctor)

    if filters.blood_type:
        query = query.filter(MedicalRecordDB.blood_type == filters.blood_type.value)

    # pagination
    return query.offset(filters.offset).limit(filters.limit).all()


# ── GET /records/{record_id} ──────────────
@router.get(
    "/{record_id}",
    summary="Get a medical record by ID",
)
async def get_record(
    _: Annotated[dict, Depends(get_current_user)],
    record: Annotated[MedicalRecordDB, Depends(get_record_or_404)]
):
    return record


# ── PUT /records/{record_id} ──────────────
@router.put(
    "/{record_id}",
    summary="Update a medical record",
)
async def update_record(
    _: Annotated[dict, Depends(get_current_user)],
    record: Annotated[MedicalRecordDB, Depends(get_record_or_404)],
    updated_record: MedicalRecord,
    db: Annotated[Session, Depends(get_db)]
):
    data = jsonable_encoder(updated_record)
    for key, value in data.items():
        setattr(record, key, value)
    db.commit()
    db.refresh(record)
    return record


# ── DELETE /records/{record_id} ───────────
@router.delete(
    "/{record_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a medical record",
)
async def delete_record(
    _: Annotated[dict, Depends(get_current_user)],
    record: Annotated[MedicalRecordDB, Depends(get_record_or_404)],
    db: Annotated[Session, Depends(get_db)]
):
    db.delete(record)
    db.commit()

    
