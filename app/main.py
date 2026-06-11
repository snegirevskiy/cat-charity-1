from fastapi import FastAPI

from app.api.charity_project import router as charity_project_router
from app.api.donation import router as donation_router

app = FastAPI(
    title='Благотворительный фонд поддержки котиков QRKot',
    description='Сервис для поддержки котиков',
    version='0.1.0',
)

app.include_router(
    charity_project_router,
    prefix='/charity_project',
    tags=['charity_projects'],
)
app.include_router(
    donation_router,
    prefix='/donation',
    tags=['donations'],
)
