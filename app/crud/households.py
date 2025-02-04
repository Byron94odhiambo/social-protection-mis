# app/crud/household.py
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from app.crud.base import CRUDBase
from app.models.household import Household
from app.schemas.household import HouseholdCreate, HouseholdUpdate
from app.core.security import encrypt_phone

class CRUDHousehold(CRUDBase[Household, HouseholdCreate, HouseholdUpdate]):
    async def create(self, db: AsyncSession, *, obj_in: HouseholdCreate) -> Household:
        """
        Create a new household with encrypted phone number.
        """
        create_data = obj_in.dict()
        phone = create_data.pop("phone")
        db_obj = Household(
            **create_data,
            encrypted_phone=encrypt_phone(phone)
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_with_members(
        self, db: AsyncSession, *, id: int
    ) -> Optional[Household]:
        """
        Get a household with its members.
        """
        stmt = (
            select(Household)
            .options(joinedload(Household.members))
            .filter(Household.id == id)
        )
        result = await db.execute(stmt)
        return result.unique().scalar_one_or_none()

    async def get_by_national_id(
        self, db: AsyncSession, *, national_id: str
    ) -> Optional[Household]:
        """
        Get a household by national ID.
        """
        stmt = select(Household).filter(Household.national_id == national_id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_program(
        self, db: AsyncSession, *, program_id: int, skip: int = 0, limit: int = 100
    ) -> List[Household]:
        """
        Get households by program.
        """
        stmt = (
            select(Household)
            .filter(Household.program_id == program_id)
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(stmt)
        return result.scalars().all()

household = CRUDHousehold(Household)