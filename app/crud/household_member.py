# app/crud/household_member.py
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.crud.base import CRUDBase
from app.models.household import HouseholdMember
from app.schemas.household import HouseholdMemberCreate, HouseholdMemberUpdate

class CRUDHouseholdMember(CRUDBase[HouseholdMember, HouseholdMemberCreate, HouseholdMemberUpdate]):
    async def get_by_household(
        self, db: AsyncSession, *, household_id: int, skip: int = 0, limit: int = 100
    ) -> List[HouseholdMember]:
        """
        Get members of a specific household.
        """
        stmt = (
            select(HouseholdMember)
            .filter(HouseholdMember.household_id == household_id)
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(stmt)
        return result.scalars().all()

    async def get_by_age_range(
        self, db: AsyncSession, *, min_age: int, max_age: int
    ) -> List[HouseholdMember]:
        """
        Get members within a specific age range.
        """
        stmt = (
            select(HouseholdMember)
            .filter(HouseholdMember.age >= min_age)
            .filter(HouseholdMember.age <= max_age)
        )
        result = await db.execute(stmt)
        return result.scalars().all()

household_member = CRUDHouseholdMember(HouseholdMember)