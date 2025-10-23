import base64
import json
import os
import pathlib
from typing import Any, Dict, List, Optional

from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from email.message import EmailMessage

ROOT = pathlib.Path(__file__).resolve().parents[1]
CREDENTIALS_PATH = "credentials.json"
TOKEN_PATH = "token.json"

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
]

def load_credentials() -> Credentials:
    creds: Optional[Credentials] = None

    if TOKEN_PATH.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            TOKEN_PATH.write_text(creds.to_json())
        else:
            if not CREDENTIALS_PATH.exists():
                raise FileNotFoundError(f"Missing credentials.json at {CREDENTIALS_PATH}")
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_PATH), SCOPES)
            creds = flow.run_local_server(port=3000, prompt="consent")
            TOKEN_PATH.write_text(creds.to_json())

    return creds

def gmail_service():
    creds = load_credentials()
    return build("gmail", "v1", credentials=creds)

def list_inbox_emails(q: Optional[str] = None, max_results: int = 5) -> List[Dict[str, Any]]:
    service = gmail_service()
    resp = service.users().messages().list(
        userId="me",
        labelIds=["INBOX"],
        q=q or None,
        maxResults=max(1, min(50, int(max_results))),
    ).execute()

    messages = resp.get("messages", []) or []
    results: List[Dict[str, Any]] = []

    for m in messages:
        msg = service.users().messages().get(
            userId="me",
            id=m["id"],
            format="metadata",
            metadataHeaders=["From", "Subject", "Date"],
        ).execute()
        headers = {h["name"]: h.get("value", "") for h in msg.get("payload", {}).get("headers", [])}
        results.append({
            "id": msg.get("id"),
            "threadId": msg.get("threadId"),
            "snippet": msg.get("snippet", ""),
            "from": headers.get("From", ""),
            "subject": headers.get("Subject", ""),
            "date": headers.get("Date", ""),
        })
    return results

def send_email(to: str, subject: str, text: str, cc: Optional[str] = None, bcc: Optional[str] = None):
    service = gmail_service()

    msg = EmailMessage()
    msg["To"] = to
    if cc:
        msg["Cc"] = cc
    if bcc:
        msg["Bcc"] = bcc
    msg["Subject"] = subject
    msg.set_content(text)

    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode("utf-8").rstrip("=")

    res = service.users().messages().send(
        userId="me",
        body={"raw": raw},
    ).execute()

    return {"id": res.get("id"), "threadId": res.get("threadId")}