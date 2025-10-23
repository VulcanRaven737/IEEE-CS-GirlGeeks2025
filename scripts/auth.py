import json
import os
import pathlib
from google_auth_oauthlib.flow import InstalledAppFlow

ROOT = pathlib.Path(__file__).resolve().parents[1]
CREDENTIALS_PATH = "credentials.json"
TOKEN_PATH = "token.json"

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
]

def main():
    if not CREDENTIALS_PATH.exists():
        raise FileNotFoundError(f"Missing credentials.json at {CREDENTIALS_PATH}")
    flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_PATH), SCOPES)
    creds = flow.run_local_server(port=3000, prompt="consent")
    TOKEN_PATH.write_text(creds.to_json())
    print(f"OAuth token saved to {TOKEN_PATH}")

if __name__ == "__main__":
    main()