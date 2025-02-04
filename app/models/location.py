# app/models/location.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models import Base

class County(Base):
    __tablename__ = "counties"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)

class SubCounty(Base):
    __tablename__ = "sub_counties"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    county_id = Column(Integer, ForeignKey("counties.id"))

class Location(Base):
    __tablename__ = "locations"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    sub_county_id = Column(Integer, ForeignKey("sub_counties.id"))

class SubLocation(Base):
    __tablename__ = "sub_locations"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    location_id = Column(Integer, ForeignKey("locations.id"))

def configure_location_relationships():
    County.sub_counties = relationship("SubCounty", back_populates="county")
    SubCounty.county = relationship("County", back_populates="sub_counties")
    SubCounty.locations = relationship("Location", back_populates="sub_county")
    Location.sub_county = relationship("SubCounty", back_populates="locations")
    Location.sub_locations = relationship("SubLocation", back_populates="location")
    SubLocation.location = relationship("Location", back_populates="sub_locations")
    SubLocation.households = relationship("Household", back_populates="sub_location")

# Call this after all models are imported
configure_location_relationships()