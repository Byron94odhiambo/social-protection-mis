# app/models/program.py
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models import Base

class Program(Base):
    __tablename__ = "programs"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

def configure_program_relationships():
    from app.models.household import Household
    Program.households = relationship("Household", back_populates="program")

# Call this after all models are imported
configure_program_relationships()