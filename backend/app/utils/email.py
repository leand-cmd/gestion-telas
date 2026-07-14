import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import current_app


class EmailNotConfiguredError(Exception):
    pass


def send_email_with_attachment(
    to: list[str], subject: str, body: str, attachment_bytes: bytes, attachment_filename: str
) -> None:
    smtp_host = current_app.config["SMTP_HOST"]
    smtp_user = current_app.config["SMTP_USER"]
    smtp_password = current_app.config["SMTP_PASSWORD"]
    smtp_from = current_app.config["SMTP_FROM"] or smtp_user

    if not smtp_host or not smtp_user or not smtp_password:
        raise EmailNotConfiguredError(
            "El envio de emails no esta configurado (faltan credenciales SMTP)"
        )

    if not to:
        raise ValueError("No hay destinatarios para el email")

    message = MIMEMultipart()
    message["From"] = smtp_from
    message["To"] = ", ".join(to)
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    part = MIMEApplication(attachment_bytes, Name=attachment_filename)
    part["Content-Disposition"] = f'attachment; filename="{attachment_filename}"'
    message.attach(part)

    with smtplib.SMTP(smtp_host, current_app.config["SMTP_PORT"]) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(smtp_from, to, message.as_string())
