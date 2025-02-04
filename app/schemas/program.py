# app/schemas/program.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ProgramCreate(BaseModel):
    name: str
    description: Optional[str] = None

    def model_dump(self):
        return {
            'name': self.name,
            'description': self.description
        }

class ProgramResponse(ProgramCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True