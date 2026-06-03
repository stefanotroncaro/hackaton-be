from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.emails._global_state import get_client, set_client
from app.emails.clients.base import BaseEmailClient
from app.emails.schema.email import Email
from tests.utils.create_user import create_user

intake_form_path = "api/v1/patients/intake-form"
invitations_path = "api/v1/patients/invitations"
intake_path = "api/v1/patients/intake"
patients_path = "api/v1/patients"
dashboard_path = "api/v1/patients/dashboard"
login_path = "api/v1/auth/login"

recipient_email = "patient@example.com"


class _CapturingEmailClient(BaseEmailClient):
    def __init__(self) -> None:
        self.sent: list[Email] = []

    def send_email(self, /, email: Email) -> None:
        self.sent.append(email)


def _login(client: TestClient, session: Session) -> None:
    provider = create_user(session)
    response = client.post(
        login_path, json={"email": provider.email, "password": "password"}
    )
    assert response.status_code == 204


def _create_invitation(client: TestClient) -> str:
    response = client.post(
        invitations_path, json={"email": recipient_email}
    )
    assert response.status_code == 201
    return response.json()["invitation_token"]


def _valid_submission() -> dict:
    return {
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane.doe@example.com",
        "date_of_birth": "1990-05-17",
        "chief_complaint": "Persistent low mood and trouble sleeping.",
        "symptom_duration": "1 to 6 months",
        "mood_rating": 4,
        "symptoms": ["Depressed mood", "Sleep disturbances"],
        "current_medications": "None",
        "suicidal_ideation": False,
    }


class TestIntakeForm:
    def test_get_intake_form_is_public(self, client: TestClient):
        response = client.get(intake_form_path)

        assert response.status_code == 200
        body = response.json()
        assert body["title"] == "Psychiatric Intake Form"
        assert body["chief_complaint"]["id"] == "chief_complaint"
        assert body["suicidal_ideation"]["type"] == "boolean"


class TestInvitations:
    def test_requires_authentication(self, client: TestClient):
        response = client.post(
            invitations_path, json={"email": recipient_email}
        )

        assert response.status_code == 401

    def test_provider_creates_invitation(
        self, client: TestClient, session: Session
    ):
        _login(client, session)

        response = client.post(
            invitations_path, json={"email": recipient_email}
        )

        assert response.status_code == 201
        body = response.json()
        assert body["invitation_token"]
        assert "invitation_token=" in body["intake_url"]

    def test_invitation_email_is_sent_with_intake_link(
        self, client: TestClient, session: Session
    ):
        _login(client, session)
        original_client = get_client()
        capturing_client = _CapturingEmailClient()
        set_client(capturing_client)
        try:
            response = client.post(
                invitations_path, json={"email": recipient_email}
            )
        finally:
            set_client(original_client)

        assert response.status_code == 201
        assert len(capturing_client.sent) == 1
        sent = capturing_client.sent[0]
        assert sent.to_emails == [recipient_email]
        assert response.json()["intake_url"] in sent.html


class TestSubmitIntake:
    def test_malformed_token_rejected(self, client: TestClient):
        response = client.post(
            intake_path,
            params={"invitation_token": "not-a-real-token"},
            json=_valid_submission(),
        )

        assert response.status_code == 422

    def test_unknown_invitation_rejected(self, client: TestClient):
        response = client.post(
            intake_path,
            params={
                "invitation_token": "00000000-0000-0000-0000-000000000000"
            },
            json=_valid_submission(),
        )

        assert response.status_code == 404

    def test_patient_registers_under_inviting_provider(
        self, client: TestClient, session: Session
    ):
        _login(client, session)
        token = _create_invitation(client)

        response = client.post(
            intake_path,
            params={"invitation_token": token},
            json=_valid_submission(),
        )

        assert response.status_code == 201
        body = response.json()
        assert body["email"] == "jane.doe@example.com"
        assert body["chief_complaint"] == (
            "Persistent low mood and trouble sleeping."
        )
        assert body["symptoms"] == ["Depressed mood", "Sleep disturbances"]
        assert body["provider_id"]

    def test_missing_required_answer_is_rejected(
        self, client: TestClient, session: Session
    ):
        _login(client, session)
        token = _create_invitation(client)
        payload = _valid_submission()
        del payload["chief_complaint"]

        response = client.post(
            intake_path,
            params={"invitation_token": token},
            json=payload,
        )

        assert response.status_code == 422


class TestListPatients:
    def test_requires_authentication(self, client: TestClient):
        response = client.get(patients_path)

        assert response.status_code == 401

    def test_provider_lists_their_patients(
        self, client: TestClient, session: Session
    ):
        _login(client, session)
        token = _create_invitation(client)
        client.post(
            intake_path,
            params={"invitation_token": token},
            json=_valid_submission(),
        )

        response = client.get(patients_path)

        assert response.status_code == 200
        body = response.json()
        assert body["total"] == 1
        assert body["data"][0]["email"] == "jane.doe@example.com"

    def test_dashboard_returns_summary(
        self, client: TestClient, session: Session
    ):
        _login(client, session)
        token = _create_invitation(client)
        client.post(
            intake_path,
            params={"invitation_token": token},
            json=_valid_submission(),
        )

        response = client.get(dashboard_path)

        assert response.status_code == 200
        body = response.json()
        assert body["total_patients"] == 1
        assert len(body["recent_patients"]) == 1
