import os
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from classifier import classify_email


SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
BASE_DIR = Path(__file__).resolve().parent
CREDENTIALS_FILE = BASE_DIR / "credentials.json"
TOKEN_FILE = BASE_DIR / "token.json"

GMAIL_QUERY = (
    "{intern internship application interview assessment "
    "recruiter recruitment hiring offer}"
)


def get_gmail_service():
    """Authenticate and return a Gmail API service."""
    if not CREDENTIALS_FILE.exists():
        raise FileNotFoundError(
            "credentials.json is missing. Add your Google OAuth "
            "Desktop app credentials to the project folder."
        )

    creds = None

    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(
            str(TOKEN_FILE), SCOPES
        )

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            str(CREDENTIALS_FILE), SCOPES
        )
        creds = flow.run_local_server(port=0)

    TOKEN_FILE.write_text(creds.to_json())

    return build("gmail", "v1", credentials=creds)


def scan_emails(max_results=100):
    """Fetch and classify matching Gmail messages."""
    service = get_gmail_service()

    response = (
        service.users()
        .messages()
        .list(
            userId="me",
            q=GMAIL_QUERY,
            maxResults=max_results,
        )
        .execute()
    )

    messages = response.get("messages", [])
    results = []

    for message in messages:
        details = (
            service.users()
            .messages()
            .get(
                userId="me",
                id=message["id"],
                format="metadata",
                metadataHeaders=["Subject", "From", "Date"],
            )
            .execute()
        )

        headers = {
            header["name"].lower(): header["value"]
            for header in details.get("payload", {}).get("headers", [])
        }

        subject = headers.get("subject", "(No subject)")
        snippet = details.get("snippet", "")
        category = classify_email(subject, snippet)

        if category:
            results.append({
                "id": message["id"],
                "subject": subject,
                "sender": headers.get("from", "Unknown sender"),
                "date": headers.get("date", ""),
                "snippet": snippet,
                "status": category,
                "link": (
                    "https://mail.google.com/mail/u/0/#all/"
                    + message["id"]
                ),
            })

    return results