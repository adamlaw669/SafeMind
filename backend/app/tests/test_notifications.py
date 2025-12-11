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
        email="notif@example.com",
        name="Notif User",
        password_hash=hash_password("password123"),
        is_verified=True,
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    token = create_access_token({"sub": str(user.id)})
    db.close()
    return {"user": user, "token": token}

class TestNotifications:
    def test_get_notifications(self, test_user):
        response = client.get(
            f"/api/notifications/?user_id={test_user['user'].id}",
            headers={"Authorization": f"Bearer {test_user['token']}"}
        )
        assert response.status_code == 200
        assert "notifications" in response.json()
    
    def test_get_notifications_unauthorized(self, test_user):
        response = client.get(
            "/api/notifications/?user_id=9999",
            headers={"Authorization": f"Bearer {test_user['token']}"}
        )
        assert response.status_code == 403
    
    def test_send_notification(self, test_user):
        response = client.post(
            "/api/notifications/send",
            headers={"Authorization": f"Bearer {test_user['token']}"}
        )
        assert response.status_code == 200
        assert response.json()["message"] == "Notification sent"
    
    def test_delete_notification(self, test_user):
        response = client.delete(
            "/api/notifications/1",
            headers={"Authorization": f"Bearer {test_user['token']}"}
        )
        assert response.status_code == 200
    
    def test_mark_as_read(self, test_user):
        response = client.put(
            "/api/notifications/1/read",
            headers={"Authorization": f"Bearer {test_user['token']}"}
        )
        assert response.status_code == 200

@pytest.fixture(autouse=True)
def cleanup():
    yield
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
