from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject


async def get_all(db: AsyncSession):
    result = await db.execute(select(CharityProject))
    return result.scalars().all()


async def create(
    db: AsyncSession,
    name: str,
    description: str,
    full_amount: int
):
    project = CharityProject(
        name=name,
        description=description,
        full_amount=full_amount
    )
    db.add(project)
    await db.flush()
    return project


async def update(
    db: AsyncSession,
    project: CharityProject,
    update_data: dict
):
    for field, value in update_data.items():
        setattr(project, field, value)

    if project.full_amount == project.invested_amount:
        project.fully_invested = True
        project.close_date = datetime.utcnow()

    await db.flush()
    return project


async def remove(db: AsyncSession, project: CharityProject):
    await db.delete(project)
    await db.flush()
    return project


async def get_open_projects(db: AsyncSession):
    result = await db.execute(
        select(CharityProject)
        .where(CharityProject.fully_invested == False)  # noqa: E712
        .order_by(CharityProject.create_date)
    )
    return result.scalars().all()
