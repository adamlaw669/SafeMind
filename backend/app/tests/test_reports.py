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

@pytest.fixture
def test_user():
    db = TestingSessionLocal()
    user = User(
        email="reporter@example.com",
        name="Reporter",
        hashed_password=hash_password("password123"),
        is_verified=True,
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    token = create_access_token({"sub": str(user.id)})
    db.close()
    return {"user": user, "token": token}

class TestReports:
    def test_create_report_success(self, test_user):
        response = client.post(
            "/api/reports/",
            json={
                "text": "I'm experiencing thoughts of self-harm",
                "location": "Home"
            },
            headers={"Authorization": f"Bearer {test_user['token']}"}
        )
        assert response.status_code == 200
        assert response.json()["text"] == "I'm experiencing thoughts of self-harm"
        assert response.json()["user_id"] == test_user["user"].id
    
    def test_create_report_empty_text(self, test_user):
        response = client.post(
            "/api/reports/",
            json={"text": "", "location": "Home"},
            headers={"Authorization": f"Bearer {test_user['token']}"}
        )
        assert response.status_code == 400
    
    def test_get_report_success(self, test_user):
        report_response = client.post(
            "/api/reports/",
            json={"text": "Test report", "location": "Test"},
            headers={"Authorization": f"Bearer {test_user['token']}"}
        )
        report_id = report_response.json()["id"]
        
        response = client.get(
            f"/api/reports/{report_id}",
            headers={"Authorization": f"Bearer {test_user['token']}"}
        )
        assert response.status_code == 200
        assert response.json()["id"] == report_id
    
    def test_get_report_not_found(self, test_user):
        response = client.get(
            "/api/reports/9999",
            headers={"Authorization": f"Bearer {test_user['token']}"}
        )
        assert response.status_code == 404
    
    def test_list_user_reports(self, test_user):
        for i in range(3):
            client.post(
                "/api/reports/",
                json={"text": f"Report {i}", "location": "Test"},
                headers={"Authorization": f"Bearer {test_user['token']}"}
            )
        
        response = client.get(
            f"/api/reports/user/{test_user['user'].id}",
            headers={"Authorization": f"Bearer {test_user['token']}"}
        )
        assert response.status_code == 200
        assert len(response.json()) == 3
    
    def test_emergency_creation(self, test_user):
        response = client.post(
            "/api/emergency/alert",
            json={
                "text": "Immediate danger - urgent help needed",
                "location": "Downtown"
            },
            headers={"Authorization": f"Bearer {test_user['token']}"}
        )
        assert response.status_code == 200
        assert response.json()["is_critical"] == True
        assert response.json()["status"] == "critical"
    
    def test_delete_own_report(self, test_user):
        report_response = client.post(
            "/api/reports/",
            json={"text": "To delete", "location": "Test"},
            headers={"Authorization": f"Bearer {test_user['token']}"}
        )
        report_id = report_response.json()["id"]
        
        response = client.delete(
            f"/api/reports/{report_id}",
            headers={"Authorization": f"Bearer {test_user['token']}"}
        )
        assert response.status_code == 200

@pytest.fixture(autouse=True)
def cleanup():
    yield
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
