from app.config.settings import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_email(to_email:str, subject:str, body:str):
    msg = Mail(
        from_email=settings.FROM_EMAIL,
        to_emails=to_email,
        subject=subject,
        plain_text_content=body
    )

    sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
    sg.send(msg)