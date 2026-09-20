# Gmail Ollama Cleanup Agent

A local Python agent that uses Ollama for intent parsing and the Gmail API for controlled email cleanup.

## Safety model

- The LLM does **not** get unrestricted Gmail access.
- Gmail operations are exposed through narrow tool functions.
- `DRY_RUN=true` previews what would be trashed.
- `CONFIRM` mode requires explicit confirmation.
- The Gmail OAuth scope is `gmail.modify`, so the app can move messages to Trash but cannot permanently delete them.
- The default model is configurable through `.env`.

## Requirements

- Python 3.11+
- Ollama running locally
- A Gmail account
- A Google Cloud OAuth Desktop App credential JSON

## 1. Create the environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 2. Configure Google OAuth

In Google Cloud Console:

1. Create/select a project.
2. Enable the Gmail API.
3. Configure the OAuth consent screen.
4. Create an OAuth Client ID for a Desktop App.
5. Download the JSON credential file.
6. Save it as:

```text
credentials/credentials.json
```

Do not commit that file.

On first run, the browser opens for Google authorization. A local `token.json` is then cached.

## 3. Configure Ollama

Start Ollama and make sure the selected model exists:

```bash
ollama pull qwen2.5:3b
```

Edit `.env` if required.

## 4. Run a dry run

```bash
cp .env.example .env
python main.py
```

Example:

```text
You: show me unread emails older than 30 days except starred
```

The agent translates the request into a constrained Gmail search query and shows a preview.

## 5. Delete by moving to Trash

Use:

```text
delete unread emails older than 30 days except starred
```

The app will show the number of matching messages and ask for confirmation.

## Supported examples

```text
show unread emails
delete unread emails
delete unread emails older than 30 days
delete unread emails older than 90 days except starred
delete unread promotional emails older than 30 days
preview unread emails from newsletters
```

The natural-language parser intentionally supports a conservative subset of Gmail cleanup operations.

## Important

"Delete" means **move to Gmail Trash**, not permanent deletion.

The app does not implement Gmail `delete`/permanent deletion.

## Tests

```bash
pytest -q
```
