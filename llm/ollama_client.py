from __future__ import annotations

import json
from typing import Any

from ollama import Client

SYSTEM_PROMPT = """You are a Gmail cleanup intent parser.

Return ONLY valid JSON with this schema:
{
  "action": "preview" | "trash" | "help",
  "gmail_query": "string",
  "reason": "string"
}

Rules:
1. Only target unread email unless the user explicitly asks for another supported condition.
2. "delete", "remove", or "trash" means action=trash.
3. "show", "list", "find", "preview" means action=preview.
4. "help" means action=help.
5. Never create a Gmail query that permanently deletes anything.
6. Preserve safety exclusions requested by the user.
7. Supported Gmail query concepts include:
   - is:unread
   - older_than:Nd
   - newer_than:Nd
   - is:starred
   - is:important
   - category:promotions
   - category:social
   - category:updates
   - from:address
   - subject:word
   - -is:starred
   - -is:important
8. If the user says "unread emails", use is:unread.
9. For "older than 30 days", use older_than:30d.
10. Never invent an email address.
11. If the request is ambiguous or outside this scope, return action=help.
12. Keep the response valid JSON with no markdown.
"""


class OllamaClient:
    def __init__(self, base_url: str, model: str) -> None:
        self.client = Client(host=base_url)
        self.model = model

    def parse_cleanup_request(self, request: str) -> dict[str, Any]:
        response = self.client.chat(
            model=self.model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": request},
            ],
            options={"temperature": 0},
        )

        content = response["message"]["content"].strip()

        if content.startswith("```"):
            content = content.replace("```json", "").replace("```", "").strip()

        data = json.loads(content)

        if not isinstance(data, dict):
            raise ValueError("Ollama returned an invalid intent.")

        return data
