<<<<<<< HEAD
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
=======
from fastapi import responses
import pytest
import warnings

from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker

from api.core.database import Base

from api.models.dto.user_dto import UserCreateDTO
from api.models.enums.roles import Roles


@pytest.fixture(scope="function")
def db_session():
    SQL_ALCHEMY_DATABASE_URL = "sqlite:///./test.db"
    engine = create_engine(
        SQL_ALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    from api.core.main import app
    from api.core.database import get_db

    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db

    from fastapi.testclient import TestClient

    with TestClient(app) as testclient:
        yield testclient

    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def auth_headers(client, db_session):
    response = client.post(
        "/auth/signup",
        json={
            "email": "email@email.com",
            "password": "testpassword123",
            "confirm_password": "testpassword123",
            "role": "user",
        },
    )

    assert response.status_code == 201

    response = client.post(
        "/auth/signin", json={"email": "email@email.com", "password": "testpassword123"}
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
>>>>>>> 2ecb84c (fix: resolve conflict)
