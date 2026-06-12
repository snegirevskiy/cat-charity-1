from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.donation import Donation


async def get_all(db: AsyncSession):
    result = await db.execute(select(Donation))
    return result.scalars().all()


async def create(
    db: AsyncSession,
    full_amount: int,
    comment: str | None = None
):
    donation = Donation(
        full_amount=full_amount,
        comment=comment,
    )
    db.add(donation)
    await db.flush()
    return donation


async def get_open_donations(db: AsyncSession):
    result = await db.execute(
        select(Donation)
        .where(Donation.fully_invested == False)  # noqa: E712
        .order_by(Donation.create_date)
    )
    return result.scalars().all()
