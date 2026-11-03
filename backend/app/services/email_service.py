import os
import re
import socket
import secrets
import smtplib
import logging
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Tuple

from app.config import settings

logger = logging.getLogger("agro_ai.email_service")

# List of common disposable/throwaway/fake email domains
DISPOSABLE_DOMAINS = {
    "mailinator.com", "tempmail.com", "10minutemail.com", "guerrillamail.com",
    "throwawaymail.com", "yopmail.com", "sharklasers.com", "dispostable.com",
    "getairmail.com", "fake.com", "test.com", "example.com", "trashmail.com",
    "maildrop.cc", "nada.ltd", "burnermail.io", "temp-mail.org", "crazymailing.com",
    "mohmal.com", "mytemp.email", "inboxkitten.com", "guerrillamailblock.com"
}

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

class EmailVerificationService:
    @staticmethod
    def is_valid_genuine_email(email: str) -> Tuple[bool, str]:
        """
        Validates that an email is structurally sound, not from a disposable service,
        and belongs to a domain with active DNS/mail exchange records.
        """
        clean_email = email.strip().lower()

        # 1. Syntax check
        if not EMAIL_REGEX.match(clean_email):
            return False, "Invalid email format. Please provide a standard address (e.g., name@domain.com)."

        domain = clean_email.split("@")[-1]

        # 2. Check for disposable or fake domains
        if domain in DISPOSABLE_DOMAINS:
            return False, "Disposable or temporary email addresses are not permitted. Please use a genuine email account."

        # 3. Check for obvious dummy patterns
        local_part = clean_email.split("@")[0]
        if local_part in ["test", "fake", "temp", "random", "nobody", "dummy"]:
            return False, "Generic placeholder emails are not accepted. Please provide your real email."

        # 4. Check DNS domain resolution
        try:
            # Check if domain resolves to an IP address
            socket.gethostbyname(domain)
        except socket.gaierror:
            return False, f"The email domain '{domain}' does not exist or cannot receive mail."
        except Exception as e:
            logger.warning(f"Domain lookup warning for {domain}: {e}")

        return True, ""

    @staticmethod
    def generate_otp(length: int = 6) -> str:
        """Generate a cryptographically secure numeric OTP."""
        return "".join(secrets.choice("0123456789") for _ in range(length))

    @classmethod
    def send_otp_email(cls, recipient_email: str, recipient_name: str, otp_code: str) -> Tuple[bool, str]:
        """
        Sends verification OTP via configured SMTP service.
        Only returns True if the SMTP server acknowledges and confirms successful message delivery.
        Does NOT return fake success or dummy responses.
        """
        smtp_server = settings.SMTP_SERVER or os.getenv("SMTP_SERVER", "smtp.gmail.com")
        smtp_port = int(settings.SMTP_PORT or os.getenv("SMTP_PORT", "587"))
        smtp_user = (settings.SMTP_USERNAME or os.getenv("SMTP_USERNAME", "")).strip()
        smtp_pass = (settings.SMTP_PASSWORD or os.getenv("SMTP_PASSWORD", "")).strip()
        from_email = (settings.SMTP_FROM_EMAIL or os.getenv("SMTP_FROM_EMAIL", "") or smtp_user).strip()
        from_name = (settings.SMTP_FROM_NAME or os.getenv("SMTP_FROM_NAME", "AGRO AI Security")).strip()

        subject = f"🌱 {otp_code} is your AGRO AI Verification Code"

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
          <meta charset="utf-8">
          <style>
            body {{ font-family: 'Segoe UI', Arial, sans-serif; background-color: #f4f6f8; margin: 0; padding: 20px; }}
            .container {{ max-width: 520px; background: #ffffff; border-radius: 16px; margin: auto; padding: 32px; border: 1px solid #e1e8ed; }}
            .header {{ text-align: center; margin-bottom: 24px; }}
            .logo {{ font-size: 24px; font-weight: 800; color: #166534; }}
            .badge {{ display: inline-block; padding: 4px 12px; background: #dcfce7; color: #166534; border-radius: 999px; font-size: 12px; font-weight: bold; margin-top: 8px; }}
            .otp-box {{ background: #f0fdf4; border: 2px dashed #22c55e; border-radius: 12px; padding: 20px; text-align: center; margin: 24px 0; }}
            .otp {{ font-size: 36px; font-weight: 800; letter-spacing: 6px; color: #15803d; }}
            .footer {{ text-align: center; font-size: 12px; color: #64748b; margin-top: 24px; }}
          </style>
        </head>
        <body>
          <div class="container">
            <div class="header">
              <div class="logo">🌱 AGRO AI</div>
              <div class="badge">Official Verification</div>
            </div>
            <p>Hello <strong>{recipient_name}</strong>,</p>
            <p>Thank you for joining AGRO AI. Use the verification code below to confirm your genuine email address and activate your account:</p>
            <div class="otp-box">
              <div class="otp">{otp_code}</div>
              <div style="font-size: 12px; color: #166534; margin-top: 6px;">Valid for 10 minutes</div>
            </div>
            <p style="font-size: 13px; color: #475569;">If you did not request this verification, please disregard this email.</p>
            <div class="footer">
              &copy; {datetime.utcnow().year} AGRO AI Platform — Smart Agriculture. Healthy Lives. Better Future.
            </div>
          </div>
        </body>
        </html>
        """

        text_content = f"Hello {recipient_name},\n\nYour AGRO AI verification code is: {otp_code}\n\nThis code expires in 10 minutes.\n\nAGRO AI Team"

        # Check SMTP configuration
        if not smtp_user or not smtp_pass:
            err = (
                "SMTP email service is not configured. "
                "Please configure SMTP_USERNAME and SMTP_PASSWORD in backend .env to send real verification emails."
            )
            logger.error(f"[AGRO AI SMTP] Delivery aborted: {err}")
            return False, err

        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = f"{from_name} <{from_email}>"
            msg["To"] = recipient_email
            msg["Reply-To"] = from_email

            msg.attach(MIMEText(text_content, "plain"))
            msg.attach(MIMEText(html_content, "html"))

            with smtplib.SMTP(smtp_server, smtp_port, timeout=15) as server:
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(smtp_user, smtp_pass)
                refused = server.sendmail(from_email, [recipient_email], msg.as_string())
                if refused:
                    err = f"Mail server refused recipient: {refused}"
                    logger.error(f"[AGRO AI SMTP] {err}")
                    return False, err

            logger.info(f"✅ OTP email successfully delivered via SMTP to {recipient_email}")
            return True, f"Verification code successfully delivered to {recipient_email}."
        except smtplib.SMTPAuthenticationError as e:
            err = "SMTP authentication failed. Please verify your SMTP_USERNAME and Google App Password."
            logger.error(f"[AGRO AI SMTP] {err} (code={e.smtp_code})")
            return False, err
        except smtplib.SMTPConnectError as e:
            err = f"Could not connect to SMTP server ({smtp_server}:{smtp_port})."
            logger.error(f"[AGRO AI SMTP] {err}")
            return False, err
        except smtplib.SMTPServerDisconnected as e:
            err = f"SMTP server disconnected unexpectedly: {e}"
            logger.error(f"[AGRO AI SMTP] {err}")
            return False, err
        except smtplib.SMTPRecipientsRefused as e:
            err = f"Recipient email was refused by the mail server: {recipient_email}"
            logger.error(f"[AGRO AI SMTP] {err}")
            return False, err
        except Exception as e:
            err = f"SMTP transmission error: {type(e).__name__} - {str(e)}"
            logger.error(f"[AGRO AI SMTP] {err}")
            return False, err

