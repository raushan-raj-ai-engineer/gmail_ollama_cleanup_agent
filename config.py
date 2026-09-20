from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    ollama_base_url: str
    ollama_model: str
    gmail_credentials_file: str
    gmail_token_file: str
    dry_run: bool
    max_messages_per_run: int

    @classmethod
    def from_env(cls) -> Settings:
        load_dotenv()
        return cls(
            ollama_base_url=os.getenv(
                "OLLAMA_BASE_URL", "http://localhost:11434"
            ),
            ollama_model=os.getenv("OLLAMA_MODEL", "qwen2.5:3b"),
            gmail_credentials_file=os.getenv(
                "GMAIL_CREDENTIALS_FILE",
                "credentials/credentials.json",
            ),
            gmail_token_file=os.getenv(
                "GMAIL_TOKEN_FILE",
                "credentials/token.json",
            ),
            dry_run=os.getenv("DRY_RUN", "true").lower() == "true",
            max_messages_per_run=int(
                os.getenv("MAX_MESSAGES_PER_RUN", "100")
            ),
        )
