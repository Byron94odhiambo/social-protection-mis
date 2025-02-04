# app/api/v1/endpoints/households.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from typing import List
from app.models import Household, HouseholdMember
from app.schemas.household import (
    HouseholdCreate, 
    HouseholdResponse, 
    HouseholdMemberCreate, 
    HouseholdMemberResponse
)
from app.core.security import encrypt_phone, decrypt_phone
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from app.api.deps import get_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/", response_model=HouseholdResponse, status_code=status.HTTP_201_CREATED)
async def create_household(
    household: HouseholdCreate, 
    db: AsyncSession = Depends(get_db)
):
    try:
        logger.info(f"Creating household for: {household.head_name}")
        
        # Create new household
        db_household = Household(
            head_name=household.head_name,
            encrypted_phone=encrypt_phone(household.phone),
            national_id=household.national_id,
            program_id=household.program_id,
            sub_location_id=household.sub_location_id
        )
        db.add(db_household)
        await db.commit()
        await db.refresh(db_household)
        
        # Create response with decrypted phone
        response = HouseholdResponse(
            id=db_household.id,
            head_name=db_household.head_name,
            phone=household.phone,
            national_id=db_household.national_id,
            program_id=db_household.program_id,
            sub_location_id=db_household.sub_location_id,
            created_at=db_household.created_at,
            members=[]
        )
        
        logger.info(f"Successfully created household with ID: {db_household.id}")
        return response
        
    except Exception as e:
        logger.error(f"Error creating household: {str(e)}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating household: {str(e)}"
        )

@router.get("/{household_id}", response_model=HouseholdResponse)
async def get_household(
    household_id: int, 
    db: AsyncSession = Depends(get_db)
):
    try:
        logger.info(f"Fetching household with ID: {household_id}")
        
        # Query household with members
        stmt = (
            select(Household)
            .options(joinedload(Household.members))
            .filter(Household.id == household_id)
        )
        result = await db.execute(stmt)
        household = result.unique().scalar_one_or_none()
        
        if household is None:
            logger.warning(f"Household not found with ID: {household_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Household not found with ID: {household_id}"
            )
        
        # Create response with decrypted phone
        response = HouseholdResponse(
            id=household.id,
            head_name=household.head_name,
            phone=decrypt_phone(household.encrypted_phone),
            national_id=household.national_id,
            program_id=household.program_id,
            sub_location_id=household.sub_location_id,
            created_at=household.created_at,
            members=[HouseholdMemberResponse.from_orm(m) for m in household.members]
        )
        
        logger.info(f"Successfully retrieved household with ID: {household_id}")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching household: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching household: {str(e)}"
        )

@router.post("/{household_id}/members/", response_model=HouseholdMemberResponse)
async def add_household_member(
    household_id: int,
    member: HouseholdMemberCreate,
    db: AsyncSession = Depends(get_db)
):
    try:
        logger.info(f"Adding member to household {household_id}: {member.name}")
        
        # Verify household exists
        stmt = select(Household).filter(Household.id == household_id)
        result = await db.execute(stmt)
        household = result.scalar_one_or_none()
        
        if not household:
            logger.warning(f"Household not found with ID: {household_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Household not found with ID: {household_id}"
            )
        
        # Create new member
        db_member = HouseholdMember(
            household_id=household_id,
            **member.model_dump()
        )
        db.add(db_member)
        await db.commit()
        await db.refresh(db_member)
        
        logger.info(f"Successfully added member {db_member.id} to household {household_id}")
        return db_member
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error adding household member: {str(e)}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error adding household member: {str(e)}"
        )