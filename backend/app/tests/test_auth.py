import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.base import Base, get_db
from app.models.user import User
from app.core.security import create_access_token, hash_password

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

class TestAuth:
    def test_signup_success(self):
        response = client.post("/api/auth/signup", json={
            "email": "test@example.com",
            "name": "Test User",
            "password": "password123"
        })
        assert response.status_code == 200
        assert "access_token" in response.json()
        assert response.json()["user"]["email"] == "test@example.com"
    
    def test_signup_duplicate_email(self):
        client.post("/api/auth/signup", json={
            "email": "duplicate@example.com",
            "name": "User One",
            "password": "password123"
        })
        response = client.post("/api/auth/signup", json={
            "email": "duplicate@example.com",
            "name": "User Two",
            "password": "password123"
        })
        assert response.status_code == 400
    
    def test_signup_missing_password(self):
        response = client.post("/api/auth/signup", json={
            "email": "nopass@example.com",
            "name": "No Pass User"
        })
        assert response.status_code == 400
    
    def test_google_login(self):
        response = client.post("/api/auth/google/login")
        assert response.status_code == 200
        assert "auth_uri" in response.json()
    
    def test_logout(self):
        response = client.post("/api/auth/logout")
        assert response.status_code == 200
        assert response.json()["message"] == "Logged out successfully"
    
    def test_verify_email(self):
        client.post("/api/auth/signup", json={
            "email": "verify@example.com",
            "name": "Verify User",
            "password": "password123"
        })
        response = client.post("/api/auth/verify-email?email=verify@example.com")
        assert response.status_code == 200
    
    def test_verify_nonexistent_email(self):
        response = client.post("/api/auth/verify-email?email=nonexistent@example.com")
        assert response.status_code == 404

@pytest.fixture(autouse=True)
def cleanup():
    yield
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
