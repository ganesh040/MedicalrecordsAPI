from enum import Enum
from pydantic import BaseModel, Field,EmailStr
from datetime import datetime




class Bloodtype(str, Enum):
    A_POSITIVE = "A+"
    A_NEGATIVE = "A-"
    B_POSITIVE = "B+"
    B_NEGATIVE = "B-"
    AB_POSITIVE = "AB+"
    AB_NEGATIVE = "AB-"
    O_POSITIVE = "O+"
    O_NEGATIVE = "O-"
    
class RecordFilter(BaseModel):
    model_config = {"extra": "forbid"}
    doctor:     str | None      = None
    blood_type: Bloodtype | None = None
    limit:int = Field(default=10, ge=1, le=100)
    offset:int = Field(default=0, ge=0)


    
class MedicalRecord(BaseModel):
    patient_name : str = Field(min_length=2, max_length=100, json_schema_extra={"example": "John Doe"})
    age : int = Field(ge=0, le=120, json_schema_extra={"example": 30})
    blood_type : Bloodtype = Field(json_schema_extra={"example": "A+"})
    diagnosis : str = Field(min_length=5, max_length=500, json_schema_extra={"example": "Hypertension"})
    doctor_id: int = Field(gt=0, json_schema_extra={"example": 1})
    email: EmailStr = Field(json_schema_extra={"example": "john.doe@example.com"})
    phone :str = Field(pattern=r'^\+?1?\d{9,15}$', json_schema_extra={"example": "+1234567890"})
    admitted_at : datetime 
    is_admitted : bool = Field(default=False)
    notes : str | None = Field(max_length=1000, json_schema_extra={"example": "Patient is responding well to treatment."})
    weight : float = Field(gt=0)
    height : float = Field(gt=0)
    