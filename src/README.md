// filepath: c:\Abhay\PES\Workshop\README_server.md
# src/server.py — Deep Dive (MCP over stdio)

Purpose
- Expose Gmail actions as MCP tools so any MCP-compatible client can call them via stdio.

Server identity
- Name: gmail-mcp
- Version: 0.1.0
- Transport: stdio (spawned subprocess)

Key imports
- mcp.server.Server and mcp.server.stdio.stdio_server for the MCP runtime.
- mcp.types.Tool to define tool metadata and input JSON Schemas.
- list_inbox_emails and send_email from gmail.py.

Handlers
1) list_tools
   - Advertises two tools:
     - list_emails
       - Input schema:
         - q: optional string (Gmail search query)
         - maxResults: number, 1–50, default 5
     - send_email
       - Required: to, subject, text
       - Optional: cc, bcc
   - Schema guides client validation and UI.

2) call_tool(name, arguments)
   - list_emails:
     - Extracts q and maxResults (default 5), calls gmail.list_inbox_emails.
     - Returns a content array with one text item containing JSON-serialized results.
   - send_email:
     - Validates required fields, calls gmail.send_email.
     - Returns status + Gmail ids as JSON in a text content item.
   - Unknown tool -> ValueError, surfaced to the client as an error response.

Runtime
- asyncio.run(main()) starts stdio_server() and awaits server.run(read, write).
- Stateless across calls; relies on gmail.py which uses token.json for auth.

Adding new tools
- Extend list_tools() with a new Tool and JSON Schema.
- Add a branch in call_tool() to implement the behavior.
- Prefer returning compact JSON via a single text content item for broad client compatibility.