import os
from email.message import EmailMessage
from email.utils import formataddr
import aiosmtplib
from dotenv import load_dotenv

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.office365.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SMTP_TITLE_NAME = os.getenv("SMTP_TITLE_NAME")

async def send_email(to_email: str, subject: str, content: str):
    message = EmailMessage()
    message["From"] = formataddr((SMTP_TITLE_NAME, SMTP_USERNAME))
    message["To"] = to_email
    message["Subject"] = subject
    message.set_content(content)

    try:
        await aiosmtplib.send(
            message,
            hostname=SMTP_HOST,
            port=SMTP_PORT,
            username=SMTP_USERNAME,
            password=SMTP_PASSWORD,
            start_tls=True,
        )
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
