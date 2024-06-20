import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, engine

# Fixture para inicializar o banco de dados de teste
@pytest.fixture(scope="module")
def db():
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    yield db
    db.close()

# Fixture para fornecer o cliente de teste para a aplicação
@pytest.fixture(scope="module")
def test_app_client():
    from fastapi.testclient import TestClient
    from app.main import app  
    client = TestClient(app)
    yield client
