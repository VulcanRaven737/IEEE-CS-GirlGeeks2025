# Meet MCP: The Cool New Way AI Remembers Stuff
IEEE CS PESU • Model Context Protocol (MCP) Workshop

A minimal MCP server that lists and sends Gmail messages via the Gmail API using Python.

## Folder structure
```
c:\Abhay\PES\Workshop
├─ credentials.json        # OAuth client (Desktop) from Google Cloud Console
├─ token.json              # Generated after auth; stores user tokens
├─ requirements.txt        # Python dependencies for this repo
├─ scripts\
│  └─ auth.py              # One-time OAuth flow; creates/updates token.json
└─ src\
   ├─ gmail.py             # Gmail API helpers (auth, list emails, send email)
   └─ server.py            # MCP stdio server exposing list_emails and send_email
```

## Prerequisites
- Python 3.9+ on Windows
- Gmail API enabled in a Google Cloud project
- OAuth client credentials (Application type: Desktop) downloaded as credentials.json

## Setup (Windows, VS Code terminal)
1) Place credentials.json in the repo root:

2) Create a virtual environment and install deps:
   - py -3 -m venv .venv
   - .venv\Scripts\activate
   - pip install -r requirements.txt

3) Authenticate (opens browser; writes token.json to repo root):
   - python scripts\auth.py

4) Run the MCP server (stdio):
   - python src\server.py

## Tools exposed
- list_emails
  - Input: { q?: string, maxResults?: number (1–50, default 5) }
  - Output: array of { id, threadId, snippet, from, subject, date }
- send_email
  - Input: { to: string, subject: string, text: string, cc?: string, bcc?: string }
  - Output: { status: "sent", id, threadId }

## Troubleshooting
- 403 insufficientPermissions: enable Gmail API and re-auth with correct scopes.
- No refresh_token: delete token.json, ensure consent screen completes fully.
- Port conflicts on 3000: close the process using the port and retry auth.
- Stdio launch issues: ensure the client’s working directory is the repo root.