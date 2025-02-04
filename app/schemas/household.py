# app/schemas/household.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

class HouseholdMemberBase(BaseModel):
    name: str = Field(..., example="John Jr")
    age: int = Field(..., example=15)
    gender: str = Field(..., example="M")
    relationship: str = Field(..., example="Son")

class HouseholdMemberCreate(HouseholdMemberBase):
    pass

class HouseholdMemberResponse(HouseholdMemberBase):
    id: int
    household_id: int

    class Config:
        from_attributes = True

class HouseholdCreate(BaseModel):
    head_name: str = Field(..., example="John Doe")
    phone: str = Field(..., example="+254722000001")
    national_id: str = Field(..., example="12345678")
    program_id: int = Field(..., example=1)
    sub_location_id: int = Field(..., example=1)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "head_name": "John Doe",
                    "phone": "+254722000001",
                    "national_id": "12345678",
                    "program_id": 1,
                    "sub_location_id": 1
                }
            ]
        }
    }

class HouseholdResponse(BaseModel):
    id: int
    head_name: str
    phone: str
    national_id: str
    program_id: int
    sub_location_id: int
    created_at: datetime
    members: List[HouseholdMemberResponse] = []

    class Config:
        from_attributes = True