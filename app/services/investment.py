from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject
from app.models.donation import Donation


async def invest_donation(db: AsyncSession, donation: Donation):
    projects = await db.execute(
        select(CharityProject)
        .where(CharityProject.fully_invested == False)  # noqa: E712
        .order_by(CharityProject.create_date)
    )
    projects = projects.scalars().all()

    remaining_amount = donation.full_amount

    for project in projects:
        if remaining_amount <= 0:
            break

        needed_amount = project.full_amount - project.invested_amount
        invest_amount = min(remaining_amount, needed_amount)

        project.invested_amount += invest_amount
        donation.invested_amount += invest_amount
        remaining_amount -= invest_amount

        if project.invested_amount >= project.full_amount:
            project.fully_invested = True
            project.close_date = datetime.utcnow()

    if donation.invested_amount >= donation.full_amount:
        donation.fully_invested = True
        donation.close_date = datetime.utcnow()


async def invest_project(db: AsyncSession, project: CharityProject):
    donations = await db.execute(
        select(Donation)
        .where(Donation.fully_invested == False)  # noqa: E712
        .order_by(Donation.create_date)
    )
    donations = donations.scalars().all()

    remaining_amount = project.full_amount

    for donation in donations:
        if remaining_amount <= 0:
            break

        available_amount = donation.full_amount - donation.invested_amount
        invest_amount = min(remaining_amount, available_amount)

        donation.invested_amount += invest_amount
        project.invested_amount += invest_amount
        remaining_amount -= invest_amount

        if donation.invested_amount >= donation.full_amount:
            donation.fully_invested = True
            donation.close_date = datetime.utcnow()

    if project.invested_amount >= project.full_amount:
        project.fully_invested = True
        project.close_date = datetime.utcnow()
