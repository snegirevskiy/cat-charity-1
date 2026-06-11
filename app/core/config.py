from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    app_title: str = "Благотворительный фонд поддержки котиков QRKot"
    app_description: str = "Сервис для поддержки котиков"
    database_url: str = "sqlite+aiosqlite:///./fastapi.db"


settings = Settings()
DATABASE_URL = settings.database_url
