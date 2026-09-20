from __future__ import annotations

from dataclasses import dataclass

from config import Settings
from gmail.client import GmailClient
from llm.ollama_client import OllamaClient
from llm.parser import CleanupIntent, parse_intent


@dataclass
class GmailCleanupAgent:
    settings: Settings
    llm: OllamaClient
    gmail: GmailClient

    def __init__(self) -> None:
        self.settings = Settings.from_env()
        self.llm = OllamaClient(
            base_url=self.settings.ollama_base_url,
            model=self.settings.ollama_model,
        )
        self.gmail = GmailClient(
            credentials_file=self.settings.gmail_credentials_file,
            token_file=self.settings.gmail_token_file,
        )

    def handle(self, request: str) -> str:
        intent_data = self.llm.parse_cleanup_request(request)
        intent = parse_intent(intent_data)

        if intent.action == "help":
            return self._help()

        messages = self.gmail.search_messages(
            query=intent.gmail_query,
            max_results=self.settings.max_messages_per_run,
        )

        if not messages:
            return f"No matching messages found.\nGmail query: {intent.gmail_query}"

        preview = self.gmail.get_preview(messages[:10])

        if intent.action == "preview":
            return self._format_preview(intent, len(messages), preview)

        if intent.action != "trash":
            return "Unsupported action."

        if self.settings.dry_run:
            return (
                self._format_preview(intent, len(messages), preview)
                + "\n\nDRY RUN is enabled. Nothing was moved to Trash."
            )

        print(self._format_preview(intent, len(messages), preview))
        confirmation = input(
            f"\nMove {len(messages)} matching message(s) to Trash? Type YES to confirm: "
        ).strip()

        if confirmation != "YES":
            return "Cancelled. No messages were changed."

        trashed = self.gmail.move_to_trash([m["id"] for m in messages])
        return f"Completed: moved {trashed} message(s) to Gmail Trash."

    @staticmethod
    def _format_preview(
        intent: CleanupIntent,
        count: int,
        preview: list[dict[str, str]],
    ) -> str:
        lines = [
            f"Action: {intent.action}",
            f"Reason: {intent.reason}",
            f"Gmail query: {intent.gmail_query}",
            f"Matching messages: {count}",
            "",
            "Preview:",
        ]
        for item in preview:
            lines.append(
                f"- {item.get('date', '')} | "
                f"{item.get('from', '')} | "
                f"{item.get('subject', '(no subject)')}"
            )
        if count > len(preview):
            lines.append(f"... and {count - len(preview)} more")
        return "\n".join(lines)

    @staticmethod
    def _help() -> str:
        return """Examples:
- show unread emails
- delete unread emails
- delete unread emails older than 30 days
- delete unread emails older than 90 days except starred
- delete unread promotional emails older than 30 days

Delete means move to Gmail Trash. Permanent deletion is not supported.
"""
