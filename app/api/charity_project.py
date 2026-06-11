from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_full_amount_gte_invested,
    check_name_unique,
    check_project_closed,
    check_project_exists,
    check_project_invested,
)
from app.core.db import get_async_session
from app.models.charity_project import CharityProject
from app.schemas.schemas import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)
from app.services.investment import invest_project

router = APIRouter()


@router.get(
    '/',
    response_model=List[CharityProjectDB],
)
async def get_all_charity_projects(
        db: AsyncSession = Depends(get_async_session),
):
    result = await db.execute(select(CharityProject))
    projects = result.scalars().all()
    return projects


@router.post(
    '/',
    response_model=CharityProjectDB,
)
async def create_charity_project(
        project: CharityProjectCreate,
        db: AsyncSession = Depends(get_async_session),
):
    await check_name_unique(project.name, db)

    new_project = CharityProject(
        name=project.name,
        description=project.description,
        full_amount=project.full_amount,
    )
    db.add(new_project)
    await db.flush()

    await invest_project(db, new_project)

    await db.commit()
    await db.refresh(new_project)
    return new_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
)
async def update_charity_project(
        project_id: int,
        update_data: CharityProjectUpdate,
        db: AsyncSession = Depends(get_async_session),
):
    project = await check_project_exists(project_id, db)
    await check_project_closed(project)

    if update_data.name is not None:
        await check_name_unique(update_data.name, db, exclude_id=project_id)

    if update_data.full_amount is not None:
        await check_full_amount_gte_invested(update_data.full_amount, project)

    update_dict = update_data.model_dump(exclude_unset=True)
    for field, value in update_dict.items():
        setattr(project, field, value)

    if project.full_amount == project.invested_amount:
        project.fully_invested = True
        project.close_date = datetime.utcnow()

    await db.commit()
    await db.refresh(project)
    return project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
)
async def delete_charity_project(
        project_id: int,
        db: AsyncSession = Depends(get_async_session),
):
    project = await check_project_exists(project_id, db)
    await check_project_invested(project)

    await db.delete(project)
    await db.commit()
    return project
