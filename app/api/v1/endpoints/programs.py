# app/api/v1/endpoints/programs.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import logging
from app.models import Program  # Updated import
from app.schemas.program import ProgramCreate, ProgramResponse
from sqlalchemy import select
from app.api.deps import get_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/", response_model=List[ProgramResponse])
async def list_programs(
    skip: int = 0, 
    limit: int = 100, 
    db: AsyncSession = Depends(get_db)
):
    try:
        logger.info("Fetching programs list")
        stmt = select(Program).offset(skip).limit(limit)
        result = await db.execute(stmt)
        programs = result.scalars().all()
        logger.info(f"Found {len(list(programs))} programs")
        return programs
    except Exception as e:
        logger.error(f"Error fetching programs: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching programs: {str(e)}"
        )

@router.post("/", response_model=ProgramResponse)
async def create_program(
    program: ProgramCreate, 
    db: AsyncSession = Depends(get_db)
):
    try:
        logger.info(f"Creating program: {program.model_dump()}")
        db_program = Program(**program.model_dump())
        db.add(db_program)
        await db.commit()
        await db.refresh(db_program)
        logger.info(f"Created program with id: {db_program.id}")
        return db_program
    except Exception as e:
        logger.error(f"Error creating program: {str(e)}")
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error creating program: {str(e)}"
        )