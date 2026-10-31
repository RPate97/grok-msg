#!/usr/bin/env python3
"""Point mcp.json at the public friend-messaging MCP server.

The committed URL uses the placeholder host <domain>. Replace it before
publishing or connecting:

    python3 scripts/set-domain.py messages.example.com

Pass the host only: no scheme, path, port, user, or secret. The script writes
https://<host>/api/mcp and prints that URL.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MCP_PATH = ROOT / "mcp.json"
PLACEHOLDER = "<domain>"
HOST = re.compile(
    r"^(?=.{1,253}$)(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,63}$"
)


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: python3 scripts/set-domain.py {PLACEHOLDER}", file=sys.stderr)
        return 2

    host = sys.argv[1].strip().lower()
    if "://" in host or "/" in host or "@" in host or ":" in host:
        print("pass the host only, for example messages.example.com", file=sys.stderr)
        return 2
    if not HOST.fullmatch(host):
        print("host must be a public DNS name", file=sys.stderr)
        return 2

    data = json.loads(MCP_PATH.read_text(encoding="utf-8"))
    try:
        server = data["mcpServers"]["friendmsg"]
    except (TypeError, KeyError):
        print("mcp.json is missing mcpServers.friendmsg", file=sys.stderr)
        return 1

    server["url"] = f"https://{host}/api/mcp"
    MCP_PATH.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(server["url"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
