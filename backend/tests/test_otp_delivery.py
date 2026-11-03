import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models.user import User

client = TestClient(app)

def test_send_otp_disposable_rejected():
    res = client.post("/api/auth/send-otp", json={"email": "throwaway@tempmail.com", "fullName": "Temp User"})
    assert res.status_code == 400
    assert "Disposable" in res.json()["detail"] or "temporary" in res.json()["detail"]

def test_send_otp_unconfigured_smtp_fails_with_503():
    # When SMTP is not configured, it must return 503 error, never a fake success!
    res = client.post("/api/auth/send-otp", json={"email": "genuinefarmer@gmail.com", "fullName": "Farmer"})
    assert res.status_code == 503
    assert "SMTP email service is not configured" in res.json()["detail"]

def test_send_otp_smtp_success():
    with patch("smtplib.SMTP") as mock_smtp:
        mock_instance = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_instance
        mock_instance.sendmail.return_value = {}  # empty dict means no refused recipients

        # Temporarily mock settings to have username and password
        with patch("app.services.email_service.settings.SMTP_USERNAME", "agroai@gmail.com"), \
             patch("app.services.email_service.settings.SMTP_PASSWORD", "mockapppass1234"), \
             patch("app.services.email_service.settings.SMTP_SERVER", "smtp.gmail.com"):

            res = client.post("/api/auth/send-otp", json={"email": "realuser99@gmail.com", "fullName": "Real User"})
            assert res.status_code == 200
            data = res.json()
            assert data["success"] is True
            assert "realuser99@gmail.com" in data["message"]

            # Verify sendmail was actually invoked
            assert mock_instance.sendmail.called
