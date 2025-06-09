import pytest
from api.core.main import app
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from api.core.database import Base, get_db


SQL_ALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="function")
async def test_engine():
    engine = create_async_engine(SQL_ALCHEMY_DATABASE_URL, echo=False)
    yield engine
    await engine.dispose()


@pytest.fixture()
async def db_session_for_test(test_engine):
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = async_sessionmaker(
        autocommit=False, autoflush=False, bind=test_engine, class_=AsyncSession
    )

    async with async_session() as session:
        yield session
        await session.rollback()
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
async def async_client(db_session_for_test: AsyncSession):
    """
    Cria um cliente de teste assíncrono para a aplicação FastAPI.
    Substitui a dependência de sessão de DB pela sessão de teste.
    """
    # Sobrescreve a dependência de DB da sua aplicação
    app.dependency_overrides[get_db] = lambda: db_session_for_test

    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

    # Limpa as sobrescrições de dependência após o teste
    app.dependency_overrides = {}
