import smtplib
from email.mime.text import MIMEText
from app.core.config import settings

def send_email(to_email: str, subject: str, html_content: str):
    msg = MIMEText(html_content, "html")
    msg["Subject"] = subject
    msg["From"] = settings.SMTP_FROM
    msg["To"] = to_email

    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.ehlo()
        server.starttls()
        server.ehlo() 
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        # server.login('boney3326@gmail.com', 'ddqvplgqkxuzqxwql')
        server.sendmail(settings.SMTP_FROM, [to_email], msg.as_string())
