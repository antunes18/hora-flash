from fastapi import responses
import pytest
import warnings

from sqlalchemy import create_engine, engine
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


def setup():
    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()
    # create test items
    db_item = mock_user_create
    session.add(db_item)
    session.commit()
    session.close()


def teardown():
    Base.metadata.drop_all(bind=engine)
