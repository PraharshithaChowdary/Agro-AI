import os
import sys
import smtplib
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from app.config import settings
from app.services.email_service import EmailVerificationService

def run_smtp_diagnostic(recipient: str = "karichetipraharshitha@gmail.com"):
    print("=" * 65)
    print("[AGRO AI] Live SMTP Delivery Diagnostic & Inspection")
    print("=" * 65)

    server = settings.SMTP_SERVER or os.getenv("SMTP_SERVER", "smtp.gmail.com")
    port = int(settings.SMTP_PORT or os.getenv("SMTP_PORT", "587"))
    user = (settings.SMTP_USERNAME or os.getenv("SMTP_USERNAME", "")).strip()
    pwd = (settings.SMTP_PASSWORD or os.getenv("SMTP_PASSWORD", "")).strip()
    from_addr = (settings.SMTP_FROM_EMAIL or os.getenv("SMTP_FROM_EMAIL", "") or user).strip()

    print(f"- SMTP Server      : {server}:{port}")
    print(f"- SMTP Username    : {user if user else '<NOT CONFIGURED>'}")
    print(f"- From Address     : {from_addr if from_addr else '<NOT CONFIGURED>'}")
    print(f"- Password Status  : {'Configured (' + str(len(pwd)) + ' chars, masked)' if pwd else '<NOT CONFIGURED>'}")
    print(f"- Target Recipient : {recipient}")
    print("-" * 65)

    if not user or not pwd:
        print("\n[RESULT] Real email delivery CANNOT proceed.")
        print("   Reason: SMTP_USERNAME or SMTP_PASSWORD is not set in .env.")
        print("\nInstructions to enable real email delivery:")
        print("   1. In your .env file, specify:")
        print(f"      SMTP_SERVER=smtp.gmail.com")
        print(f"      SMTP_PORT=587")
        print(f"      SMTP_USERNAME={recipient}")
        print(f"      SMTP_PASSWORD=your_16_char_google_app_password")
        print(f"      SMTP_FROM_EMAIL={recipient}")
        print("   2. For Gmail accounts:")
        print("      - Visit https://myaccount.google.com/security")
        print("      - Enable '2-Step Verification'")
        print("      - Go to 'App passwords' (https://myaccount.google.com/apppasswords)")
        print("      - Create an app password for 'AGRO AI'")
        print("      - Paste the 16-character code into SMTP_PASSWORD in .env")
        print("=" * 65)
        return False

    print("\n[Step 1/3] Testing TCP connectivity to SMTP host...")
    try:
        with smtplib.SMTP(server, port, timeout=10) as s:
            print(f"  [OK] Connected to {server}:{port}")
            print("\n[Step 2/3] Initiating TLS handshake (STARTTLS)...")
            s.ehlo()
            s.starttls()
            s.ehlo()
            print("  [OK] TLS handshake successful and connection encrypted.")

            print("\n[Step 3/3] Authenticating with mail provider...")
            try:
                s.login(user, pwd)
                print(f"  [OK] Authenticated successfully as {user}.")
            except smtplib.SMTPAuthenticationError as e:
                print(f"  [FAIL] Authentication rejected by mail server:")
                print(f"     Code: {e.smtp_code}")
                print(f"     Detail: {e.smtp_error.decode('utf-8', errors='replace') if isinstance(e.smtp_error, bytes) else str(e.smtp_error)}")
                return False

            print(f"\n[Delivery] Dispatching real test OTP to {recipient}...")
            otp_code = EmailVerificationService.generate_otp(6)
            success, msg = EmailVerificationService.send_otp_email(recipient, "Harshi", otp_code)
            if success:
                print(f"\n[SUCCESS] Mail server confirmed delivery to {recipient}!")
                print(f"   Provider confirmation: {msg}")
                print(f"   Generated OTP: {otp_code}")
                print("   Check your inbox / spam folder for the email.")
                return True
            else:
                print(f"\n[FAILED] Provider rejected delivery: {msg}")
                return False

    except Exception as e:
        print(f"  ❌ Network/Connection error: {e}")
        return False

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "karichetipraharshitha@gmail.com"
    run_smtp_diagnostic(target)
