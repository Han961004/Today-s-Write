import asyncio
from logging.config import fileConfig

from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context

from database import DATABASE_URL, Base
from models import Post  # ✅ Post 모델 명시적으로 import

# Alembic 설정 파일 로드
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ✅ SQLAlchemy 모델의 MetaData 지정 (자동 마이그레이션 지원)
target_metadata = Base.metadata

# ✅ 비동기 DB 엔진 생성
engine = create_async_engine(DATABASE_URL, echo=True)


def run_migrations_offline() -> None:
    """오프라인 모드에서 마이그레이션 실행 (엔진 없이 URL만 사용)"""
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """온라인 모드에서 마이그레이션 실행 (비동기 엔진 사용)"""
    async with engine.connect() as connection:
        await connection.run_sync(do_run_migrations)


def do_run_migrations(connection):
    """마이그레이션 실행 (비동기 지원)"""
    context.configure(
        connection=connection, target_metadata=target_metadata
    )
    with context.begin_transaction():
        context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())  # ✅ 비동기 실행
