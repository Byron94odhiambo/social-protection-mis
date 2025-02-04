# app/models/__init__.py
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import registry

# Create registry
mapper_registry = registry()
Base = mapper_registry.generate_base()

# Import models
from app.models.program import Program
from app.models.location import County, SubCounty, Location, SubLocation
from app.models.household import Household, HouseholdMember

# Configure relationships after all models are loaded
mapper_registry.configure()