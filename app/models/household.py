# app/models/household.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models import Base

class Household(Base):
    __tablename__ = "households"
    
    id = Column(Integer, primary_key=True, index=True)
    program_id = Column(Integer, ForeignKey("programs.id"))
    sub_location_id = Column(Integer, ForeignKey("sub_locations.id"))
    head_name = Column(String(100), nullable=False)
    encrypted_phone = Column(String(255), nullable=False)
    national_id = Column(String(20), nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class HouseholdMember(Base):
    __tablename__ = "household_members"
    
    id = Column(Integer, primary_key=True, index=True)
    household_id = Column(Integer, ForeignKey("households.id"))
    name = Column(String(100), nullable=False)
    age = Column(Integer)
    gender = Column(String(10))
    relationship = Column(String(50))

def configure_household_relationships():
    Household.program = relationship("Program", back_populates="households")
    Household.sub_location = relationship("SubLocation", back_populates="households")
    Household.members = relationship("HouseholdMember", back_populates="household")
    HouseholdMember.household = relationship("Household", back_populates="members")

# Call this after all models are imported
configure_household_relationships()