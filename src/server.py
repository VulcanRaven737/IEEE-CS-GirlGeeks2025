import asyncio
import json
from typing import Any, Dict, List

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool

from .gmail import list_inbox_emails, send_email

server = Server("gmail-mcp", "0.1.0")

@server.list_tools()
async def list_tools() -> List[Tool]:
    return [
        Tool(
            name="list_emails",
            description="List recent emails from your Gmail inbox. Optional Gmail query string and maxResults.",
            input_schema={
                "type": "object",
                "properties": {
                    "q": {"type": "string", "description": "Gmail query, e.g., from:alice subject:report"},
                    "maxResults": {"type": "number", "minimum": 1, "maximum": 50, "default": 5},
                },
                "additionalProperties": False,
            },
        ),
        Tool(
            name="send_email",
            description="Send a simple text email via Gmail.",
            input_schema={
                "type": "object",
                "required": ["to", "subject", "text"],
                "properties": {
                    "to": {"type": "string", "description": "Recipient email"},
                    "subject": {"type": "string"},
                    "text": {"type": "string", "description": "Plain text body"},
                    "cc": {"type": "string", "description": "Optional CC addresses (comma-separated)"},
                    "bcc": {"type": "string", "description": "Optional BCC addresses (comma-separated)"},
                },
                "additionalProperties": False,
            },
        ),
    ]

@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]):
    if name == "list_emails":
        q = arguments.get("q")
        max_results = int(arguments.get("maxResults", 5))
        items = list_inbox_emails(q=q, max_results=max_results)
        return [{"type": "text", "text": json.dumps(items, indent=2)}]

    if name == "send_email":
        to = arguments.get("to")
        subject = arguments.get("subject")
        text = arguments.get("text")
        cc = arguments.get("cc")
        bcc = arguments.get("bcc")

        if not to or not subject or not text:
            raise ValueError("Missing required fields: to, subject, text")

        result = send_email(to=to, subject=subject, text=text, cc=cc, bcc=bcc)
        return [{"type": "text", "text": json.dumps({"status": "sent", **result}, indent=2)}]

    raise ValueError(f"Unknown tool: {name}")

async def main():
    async with stdio_server() as (read, write):
        await server.run(read, write)

if __name__ == "__main__":
    asyncio.run(main())