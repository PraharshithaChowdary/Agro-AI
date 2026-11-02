import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models.user import User

client = TestClient(app)

@pytest.fixture(autouse=True)
def cleanup_test_users():
    yield
    # Cleanup any test created accounts
    db = SessionLocal()
    try:
        db.query(User).filter(User.email.like("%@testsuite.com")).delete(synchronize_session=False)
        db.commit()
    except Exception:
        db.rollback()
    finally:
        db.close()

def test_signup_successful():
    email = "newfarmer@testsuite.com"
    response = client.post(
        "/api/auth/signup",
        json={
            "fullName": "Test Farmer",
            "email": email,
            "password": "SecurePassword123",
            "role": "farmer"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert "token" in data
    assert data["user"]["email"] == email
    assert data["user"]["role"] == "farmer"

def test_signup_admin_blocked():
    response = client.post(
        "/api/auth/signup",
        json={
            "fullName": "Fake Admin",
            "email": "hacker@testsuite.com",
            "password": "SecurePassword123",
            "role": "admin"
        }
    )
    assert response.status_code == 403

def test_signup_duplicate_email():
    email = "duplicate@testsuite.com"
    payload = {
        "fullName": "First User",
        "email": email,
        "password": "SecurePassword123",
        "role": "farmer"
    }
    res1 = client.post("/api/auth/signup", json=payload)
    assert res1.status_code == 201

    res2 = client.post("/api/auth/signup", json=payload)
    assert res2.status_code == 400

def test_login_existing_user():
    email = "existing@testsuite.com"
    password = "CorrectPassword123"
    signup_res = client.post(
        "/api/auth/signup",
        json={
            "fullName": "Existing User",
            "email": email,
            "password": password,
            "role": "farmer"
        }
    )
    assert signup_res.status_code == 201

    # Login with correct password
    login_res = client.post(
        "/api/auth/login",
        json={"email": email, "password": password}
    )
    assert login_res.status_code == 200
    data = login_res.json()
    assert "token" in data
    assert data["user"]["email"] == email

    # Login with wrong password
    bad_login = client.post(
        "/api/auth/login",
        json={"email": email, "password": "WrongPassword999"}
    )
    assert bad_login.status_code == 401

def test_login_does_not_create_unknown_accounts():
    email = "autoregister@testsuite.com"
    response = client.post(
        "/api/auth/login",
        json={"email": email, "password": "MyPassword123"}
    )
    assert response.status_code == 401
    db = SessionLocal()
    try:
        assert db.query(User).filter(User.email == email).first() is None
    finally:
        db.close()


def test_get_me_flow():
    email = "profiletest@testsuite.com"
    password = "Password123"
    signup_res = client.post(
        "/api/auth/signup",
        json={
            "fullName": "Profile User",
            "email": email,
            "password": password,
            "role": "buyer"
        }
    )
    token = signup_res.json()["token"]

    # Authenticated request
    me_res = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me_res.status_code == 200
    assert me_res.json()["user"]["email"] == email

    # Unauthenticated request
    anon_res = client.get("/api/auth/me")
    assert anon_res.status_code == 401


def test_unknown_login_does_not_create_account():
    email = "unknown-login@testsuite.com"
    response = client.post("/api/auth/login", json={"email": email, "password": "Password123"})
    assert response.status_code == 401
    db = SessionLocal()
    try:
        assert db.query(User).filter(User.email == email).first() is None
    finally:
        db.close()
