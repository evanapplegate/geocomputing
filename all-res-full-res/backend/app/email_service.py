from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from app.config import settings
from typing import Optional


def send_email(to_email: str, subject: str, html_content: str) -> bool:
    """Send email via SendGrid"""
    if not settings.email_api_key:
        print(f"Email not configured. Would send to {to_email}: {subject}")
        return False
    
    try:
        message = Mail(
            from_email=settings.email_from,
            to_emails=to_email,
            subject=subject,
            html_content=html_content
        )
        sg = SendGridAPIClient(settings.email_api_key)
        response = sg.send(message)
        return response.status_code == 202
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


def send_password_reset_email(email: str, reset_token: str) -> bool:
    """Send password reset email"""
    reset_url = f"{settings.frontend_url}/reset-password?token={reset_token}"
    html_content = f"""
    <html>
        <body>
            <h2>Password Reset Request</h2>
            <p>Click the link below to reset your password:</p>
            <p><a href="{reset_url}">{reset_url}</a></p>
            <p>This link expires in 24 hours.</p>
        </body>
    </html>
    """
    return send_email(email, "Reset Your Password - All Res Full Res", html_content)


def send_email_verification(email: str, verification_token: str) -> bool:
    """Send email verification"""
    verify_url = f"{settings.frontend_url}/verify-email?token={verification_token}"
    html_content = f"""
    <html>
        <body>
            <h2>Verify Your Email</h2>
            <p>Click the link below to verify your email address:</p>
            <p><a href="{verify_url}">{verify_url}</a></p>
        </body>
    </html>
    """
    return send_email(email, "Verify Your Email - All Res Full Res", html_content)
