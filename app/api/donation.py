from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.models.donation import Donation
from app.schemas.schemas import (
    DonationCreate,
    DonationDB,
    DonationFullInfoDB,
)
from app.services.investment import invest_donation

router = APIRouter()


@router.get(
    '/',
    response_model=List[DonationFullInfoDB],
)
async def get_all_donations(
        db: AsyncSession = Depends(get_async_session),
):
    result = await db.execute(select(Donation))
    donations = result.scalars().all()
    return donations


@router.post(
    '/',
    response_model=DonationDB,
)
async def create_donation(
        donation: DonationCreate,
        db: AsyncSession = Depends(get_async_session),
):
    new_donation = Donation(
        full_amount=donation.full_amount,
        comment=donation.comment,
    )
    db.add(new_donation)
    await db.flush()

    await invest_donation(db, new_donation)

    await db.commit()
    await db.refresh(new_donation)
    return new_donation
