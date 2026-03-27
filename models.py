from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy.sql import func


class Doctor(Base):
    __tablename__ = "doctors"

    id             = Column(Integer, primary_key=True, index=True)
    name           = Column(String(100), nullable=False)
    email          = Column(String(255), nullable=False, unique=True)
    specialization = Column(String(100), nullable=False)
    phone          = Column(String(20), nullable=True)
    created_at     = Column(DateTime(timezone=True), server_default=func.now())

    # relationship — one doctor has many records
    records = relationship("MedicalRecord", back_populates="doctor_info")
    
    
class MedicalRecord(Base):
    __tablename__ = "medical_records"

    id           = Column(Integer, primary_key=True, index=True)
    patient_name = Column(String(100), nullable=False)
    age          = Column(Integer, nullable=False)
    blood_type   = Column(String(5), nullable=False)
    diagnosis    = Column(String(500), nullable=False)
    doctor_id    = Column(Integer, ForeignKey("doctors.id"), nullable=False)  # ← replaces doctor string
    email        = Column(String(255), nullable=False)
    phone        = Column(String(20), nullable=False)
    admitted_at  = Column(DateTime(timezone=True), nullable=False)
    is_admitted  = Column(Boolean, default=False)
    notes        = Column(String(1000), nullable=True)
    weight       = Column(Float, nullable=False)
    height       = Column(Float, nullable=False)
    created_at   = Column(DateTime(timezone=True), server_default=func.now())
    updated_at   = Column(DateTime(timezone=True), onupdate=func.now())

    # relationship — many records belong to one doctor
    doctor_info  = relationship("Doctor", back_populates="records")