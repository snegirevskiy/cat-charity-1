from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import get_open_projects
from app.crud.donation import get_open_donations
from app.models.charity_project import CharityProject
from app.models.donation import Donation


async def invest_donation(db: AsyncSession, donation: Donation):
    projects = await get_open_projects(db)

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
    donations = await get_open_donations(db)

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
