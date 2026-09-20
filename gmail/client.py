from __future__ import annotations

import os
from typing import Any

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]


class GmailClient:
    def __init__(self, credentials_file: str, token_file: str) -> None:
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.service = self._build_service()

    def _build_service(self) -> Any:
        creds = None

        if os.path.exists(self.token_file):
            creds = Credentials.from_authorized_user_file(self.token_file, SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(self.credentials_file):
                    raise FileNotFoundError(
                        f"Missing Gmail OAuth credentials: {self.credentials_file}"
                    )

                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, SCOPES
                )
                creds = flow.run_local_server(port=0)

            os.makedirs(os.path.dirname(self.token_file) or ".", exist_ok=True)
            with open(self.token_file, "w", encoding="utf-8") as token:
                token.write(creds.to_json())

        return build("gmail", "v1", credentials=creds)

    def search_messages(self, query: str, max_results: int) -> list[dict[str, Any]]:
        results: list[dict[str, Any]] = []
        page_token = None

        while len(results) < max_results:
            response = (
                self.service
                .users()
                .messages()
                .list(
                    userId="me",
                    q=query,
                    maxResults=min(100, max_results - len(results)),
                    pageToken=page_token,
                )
                .execute()
            )

            results.extend(response.get("messages", []))
            page_token = response.get("nextPageToken")

            if not page_token or not response.get("messages"):
                break

        return results[:max_results]

    def get_preview(self, messages: list[dict[str, Any]]) -> list[dict[str, str]]:
        preview = []

        for message in messages:
            data = (
                self.service
                .users()
                .messages()
                .get(
                    userId="me",
                    id=message["id"],
                    format="metadata",
                    metadataHeaders=["Subject", "From", "Date"],
                )
                .execute()
            )

            headers = {
                h["name"].lower(): h["value"]
                for h in data.get("payload", {}).get("headers", [])
            }

            preview.append({
                "id": message["id"],
                "subject": headers.get("subject", ""),
                "from": headers.get("from", ""),
                "date": headers.get("date", ""),
            })

        return preview

    def move_to_trash(self, message_ids: list[str]) -> int:
        if not message_ids:
            return 0

        total = 0

        for start in range(0, len(message_ids), 1000):
            batch = message_ids[start : start + 1000]
            self.service.users().messages().batchModify(
                userId="me",
                body={
                    "ids": batch,
                    "addLabelIds": ["TRASH"],
                },
            ).execute()
            total += len(batch)

        return total
