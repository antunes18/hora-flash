# tests/conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from api.core.database import Base, get_db
from api.core.main import app
from httpx import Client

# Usando SQLite em memória para testes
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

# Engine síncrono
engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Session factory
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session_for_test():
    # Cria as tabelas
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def async_client(db_session_for_test: Session):
    """
    Cria um cliente de teste para a aplicação FastAPI.
    Substitui a dependência de sessão de DB pela sessão de teste.
    """

    # Sobrescreve a dependência de DB
    def override_get_db():
        yield db_session_for_test

    app.dependency_overrides[get_db] = override_get_db

    with Client(app=app, base_url="http://test") as client:
        yield client

    app.dependency_overrides = {}

