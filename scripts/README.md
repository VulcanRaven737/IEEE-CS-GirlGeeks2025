# scripts/auth.py — Deep Dive

Purpose
- Run the installed-app OAuth flow to obtain user consent and generate token.json for Gmail access.

What it does
- Loads the Desktop OAuth client from credentials.json.
- Starts a local loopback server on port 3000 and opens a browser to Google’s consent page.
- Exchanges the authorization code for access/refresh tokens.
- Saves the tokens to token.json at the repo root.

Key constants
- SCOPES:
  - https://www.googleapis.com/auth/gmail.readonly
  - https://www.googleapis.com/auth/gmail.send
- credentials.json: client_id and client_secret from Google Cloud Console (Desktop app).
- token.json: user tokens (access + refresh + expiry), created/updated by the script.

Flow steps
1) Validate credentials.json exists at the repo root.
2) Initialize InstalledAppFlow.from_client_secrets_file(credentials.json, SCOPES).
3) run_local_server(port=3000, prompt="consent") launches a loopback server and opens your browser.
4) On consent, Google redirects back to localhost; the script exchanges the code for tokens.
5) Write the serialized credentials JSON to token.json for later reuse.

Inputs/Outputs
- Input: credentials.json (downloaded from Google Cloud Console).
- Output: token.json (generated; contains access_token, refresh_token when issued, expiry, scopes).

Common pitfalls
- Missing refresh_token: delete token.json and re-run; ensure first-time consent for the requested scopes.
- 400 redirect errors: ensure the OAuth client “Application type” is Desktop (no custom redirect URIs needed).
- Port already in use: free port 3000 or temporarily change the port used by run_local_server.

Security
- token.json grants access to your Gmail; do not commit it.
- Keep credentials.json private (contains your client secret).
