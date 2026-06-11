from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject


async def check_project_exists(project_id: int, db: AsyncSession):
    project = await db.execute(
        select(CharityProject).where(CharityProject.id == project_id)
    )
    project = project.scalar()
    if not project:
        raise HTTPException(status_code=404, detail='Проект не найден!')
    return project


async def check_project_closed(project: CharityProject):
    if project.fully_invested:
        raise HTTPException(
            status_code=400,
            detail='Закрытый проект нельзя редактировать!',
        )


async def check_project_invested(project: CharityProject):
    if project.invested_amount > 0:
        raise HTTPException(
            status_code=400,
            detail='В проект были внесены средства, не подлежит удалению!',
        )


async def check_name_unique(
        name: str, db: AsyncSession, exclude_id: int = None
):
    query = select(CharityProject).where(CharityProject.name == name)
    if exclude_id:
        query = query.where(CharityProject.id != exclude_id)

    existing = await db.execute(query)
    if existing.scalar():
        raise HTTPException(
            status_code=400,
            detail='Проект с таким именем уже существует!',
        )


async def check_full_amount_gte_invested(
        full_amount: int, project: CharityProject
):
    if full_amount < project.invested_amount:
        raise HTTPException(
            status_code=400,
            detail=(
                'Нелья установить значение full_amount '
                'меньше уже вложенной суммы.'
            ),
        )
