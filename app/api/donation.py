from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.donation import create, get_all
from app.schemas.schemas import (
    DonationCreate,
    DonationDB,
    DonationFullInfoDB,
)
from app.services.investment import invest_donation

router = APIRouter()


@router.get('/', response_model=list[DonationFullInfoDB])
async def get_all_donations(
    db: AsyncSession = Depends(get_async_session),
):
    return await get_all(db)


@router.post('/', response_model=DonationDB)
async def create_donation(
    donation: DonationCreate,
    db: AsyncSession = Depends(get_async_session),
):
    new_donation = await create(
        db, donation.full_amount, donation.comment
    )
    await invest_donation(db, new_donation)
    await db.commit()
    await db.refresh(new_donation)
    return new_donation
