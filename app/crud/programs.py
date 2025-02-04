# app/crud/program.py
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.crud.base import CRUDBase
from app.models.program import Program
from app.schemas.program import ProgramCreate, ProgramUpdate

class CRUDProgram(CRUDBase[Program, ProgramCreate, ProgramUpdate]):
    async def get_by_name(self, db: AsyncSession, *, name: str) -> Optional[Program]:
        """
        Get a program by name.
        """
        stmt = select(Program).filter(Program.name == name)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_active_programs(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[Program]:
        """
        Get all active programs.
        """
        stmt = select(Program).offset(skip).limit(limit)
        result = await db.execute(stmt)
        return result.scalars().all()

program = CRUDProgram(Program)