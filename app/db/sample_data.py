# app/db/sample_data.py
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.db.session import engine, AsyncSessionLocal
from app.models import Base, mapper_registry
from app.models.program import Program
from app.models.location import County, SubCounty, Location, SubLocation
from app.models.household import Household, HouseholdMember
from app.core.security import encrypt_phone
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_tables():
    try:
        logger.info("Starting to create tables...")
        async with engine.begin() as conn:
            logger.info("Dropping all tables...")
            await conn.run_sync(Base.metadata.drop_all)
            logger.info("Creating all tables...")
            mapper_registry.configure()
            await conn.run_sync(Base.metadata.create_all)
            logger.info("Tables created successfully!")
    except Exception as e:
        logger.error(f"Error creating tables: {str(e)}")
        raise

async def insert_sample_data():
    async with AsyncSessionLocal() as session:
        try:
            # Programs (5 records)
            programs = [
                Program(name="Cash Transfer for Orphans", description="Support for orphaned children"),
                Program(name="Elderly Support", description="Cash transfer for elderly citizens"),
                Program(name="Disability Support", description="Support for persons with disabilities"),
                Program(name="Hunger Safety Net", description="Food security program"),
                Program(name="Urban Food Subsidy", description="Support for urban poor")
            ]
            
            logger.info("Adding programs...")
            session.add_all(programs)
            await session.commit()

            # Counties and Sub-counties (5 counties, 5 sub-counties)
            counties = [
                County(name="Nairobi", sub_counties=[
                    SubCounty(name="Westlands")
                ]),
                County(name="Mombasa", sub_counties=[
                    SubCounty(name="Nyali")
                ]),
                County(name="Kisumu", sub_counties=[
                    SubCounty(name="Kisumu Central")
                ]),
                County(name="Nakuru", sub_counties=[
                    SubCounty(name="Nakuru Town East")
                ]),
                County(name="Kiambu", sub_counties=[
                    SubCounty(name="Thika")
                ])
            ]
            
            logger.info("Adding counties and sub-counties...")
            session.add_all(counties)
            await session.commit()

            # Locations (5 records)
            locations = [
                Location(name="Location1", sub_county_id=1),
                Location(name="Location2", sub_county_id=2),
                Location(name="Location3", sub_county_id=3),
                Location(name="Location4", sub_county_id=4),
                Location(name="Location5", sub_county_id=5)
            ]
            session.add_all(locations)
            await session.commit()

            # Sub-locations (5 records)
            sub_locations = [
                SubLocation(name="SubLocation1", location_id=1),
                SubLocation(name="SubLocation2", location_id=2),
                SubLocation(name="SubLocation3", location_id=3),
                SubLocation(name="SubLocation4", location_id=4),
                SubLocation(name="SubLocation5", location_id=5)
            ]
            session.add_all(sub_locations)
            await session.commit()

            # Households and Members (5 households with members)
            households_data = [
                {
                    "head_name": "John Doe",
                    "phone": "+254722000001",
                    "national_id": "12345678",
                    "program_id": 1,
                    "sub_location_id": 1,
                    "members": [
                        {"name": "John Jr", "age": 15, "gender": "M", "relationship": "Son"},
                        {"name": "Jane Doe", "age": 13, "gender": "F", "relationship": "Daughter"}
                    ]
                },
                {
                    "head_name": "Jane Smith",
                    "phone": "+254722000002",
                    "national_id": "12345679",
                    "program_id": 2,
                    "sub_location_id": 2,
                    "members": [
                        {"name": "James Smith", "age": 10, "gender": "M", "relationship": "Son"}
                    ]
                },
                {
                    "head_name": "Alice Johnson",
                    "phone": "+254722000003",
                    "national_id": "12345680",
                    "program_id": 3,
                    "sub_location_id": 3,
                    "members": [
                        {"name": "Bob Johnson", "age": 8, "gender": "M", "relationship": "Son"}
                    ]
                },
                {
                    "head_name": "David Wilson",
                    "phone": "+254722000004",
                    "national_id": "12345681",
                    "program_id": 4,
                    "sub_location_id": 4,
                    "members": [
                        {"name": "Sarah Wilson", "age": 12, "gender": "F", "relationship": "Daughter"}
                    ]
                },
                {
                    "head_name": "Mary Brown",
                    "phone": "+254722000005",
                    "national_id": "12345682",
                    "program_id": 5,
                    "sub_location_id": 5,
                    "members": [
                        {"name": "Tom Brown", "age": 7, "gender": "M", "relationship": "Son"}
                    ]
                }
            ]

            for household_data in households_data:
                members_data = household_data.pop("members")
                household = Household(
                    head_name=household_data["head_name"],
                    encrypted_phone=encrypt_phone(household_data["phone"]),
                    national_id=household_data["national_id"],
                    program_id=household_data["program_id"],
                    sub_location_id=household_data["sub_location_id"]
                )
                session.add(household)
                await session.flush()
                
                for member_data in members_data:
                    member = HouseholdMember(
                        household_id=household.id,
                        **member_data
                    )
                    session.add(member)
                
                await session.commit()
                logger.info(f"Added household {household.head_name} with ID {household.id}")

            logger.info("Sample data inserted successfully!")
            
            # Verify final counts
            tables = ['programs', 'counties', 'sub_counties', 'locations', 
                     'sub_locations', 'households', 'household_members']
            for table in tables:
                result = await session.execute(text(f"SELECT COUNT(*) FROM {table}"))
                count = result.scalar()
                logger.info(f"Final count for {table}: {count}")
            
        except Exception as e:
            logger.error(f"Error inserting sample data: {str(e)}")
            await session.rollback()
            raise
        finally:
            await session.close()

async def main():
    try:
        await create_tables()
        logger.info("Tables created successfully, proceeding to insert sample data...")
        await insert_sample_data()
    finally:
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(main())