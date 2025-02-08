from pydantic_settings import BaseSettings  # ✅ 변경된 import 경로

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:0000@localhost:5432/app_fast"
    SECRET_KEY: str = 'django-insecure-+&2r64c8n7j&xc=q1x=@dt3kiq!8=_y&5ux$li+(0ndw_r$=5$'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 3000

    class Config:
        env_file = ".env"

settings = Settings()
