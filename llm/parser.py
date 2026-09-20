from __future__ import annotations

from dataclasses import dataclass

ALLOWED_ACTIONS = {"preview", "trash", "help"}


@dataclass(frozen=True)
class CleanupIntent:
    action: str
    gmail_query: str
    reason: str


def parse_intent(data: dict) -> CleanupIntent:
    action = str(data.get("action", "help")).lower()
    query = str(data.get("gmail_query", "")).strip()
    reason = str(data.get("reason", "")).strip()

    if action not in ALLOWED_ACTIONS:
        return CleanupIntent(
            action="help",
            gmail_query="",
            reason="Unsupported action returned by the model.",
        )

    if action != "help":
        query = _validate_query(query)

    return CleanupIntent(
        action=action,
        gmail_query=query,
        reason=reason or "Parsed by Ollama.",
    )


def _validate_query(query: str) -> str:
    if not query:
        raise ValueError("The model returned an empty Gmail query.")

    # Conservative guardrails. The application only supports cleanup
    # searches that contain unread mail for this first version.
    if "is:unread" not in query:
        raise ValueError(
            "Safety check failed: cleanup queries must contain is:unread."
        )

    forbidden = (
        "in:anywhere",
        "is:chat",
    )

    if any(term in query for term in forbidden):
        raise ValueError("Safety check rejected the Gmail query.")

    return query
