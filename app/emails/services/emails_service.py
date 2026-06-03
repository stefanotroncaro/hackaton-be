from enum import Enum
from string import Template

from app.users.schemas.user_schema import UserInDB
from app.emails.clients.base import BaseEmailClient
from app.emails.schema.email import Email
from app.emails._global_state import get_client


class Paths(Enum):
    NEW_USER = "app/emails/templates/welcome_email.html"
    INTAKE_INVITATION = "app/emails/templates/intake_invitation_email.html"


class EmailService:
    def __init__(self, email_client: BaseEmailClient | None = None):
        self.email_client = email_client or get_client()

    def _get_email(
        self,
        recipient_email: str,
        template: str,
        subject: str,
        html_message_input: dict | None = None,
    ) -> Email:
        with open(template, "r") as file:
            html_template_string = file.read()

        html_message_input = html_message_input or {}
        html = Template(html_template_string).substitute(**html_message_input)

        return Email(
            to_emails=[recipient_email],
            subject=subject,
            html=html,
        )

    def send_new_user_email(
        self,
        user: UserInDB,
    ) -> None:
        email = self._get_email(
            user.email,
            Paths.NEW_USER.value,
            "Welcome",
        )

        return self.email_client.send_email(email)

    def send_user_remind_email(
        self,
        user: UserInDB,
    ) -> None:
        email = self._get_email(
            user.email,
            Paths.NEW_USER.value,
            "Welcome",
        )

        return self.email_client.send_email(email)

    def send_intake_invitation_email(
        self,
        recipient_email: str,
        intake_url: str,
    ) -> None:
        email = self._get_email(
            recipient_email,
            Paths.INTAKE_INVITATION.value,
            "You have been invited to complete your intake form",
            {"intake_url": intake_url},
        )

        return self.email_client.send_email(email)
