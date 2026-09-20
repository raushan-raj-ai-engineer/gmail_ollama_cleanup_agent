# 🧹 Gmail Ollama Cleanup Agent

> **Clean your Gmail using natural language — privately, locally, and safely with Ollama.**

Turn simple instructions like:

> 💬 **"Delete unread emails older than 30 days except starred emails."**

into a controlled Gmail cleanup operation powered by a **local LLM**.

No cloud LLM API is required.
No OpenAI API key.
No Gemini API key.
Your natural-language request is interpreted locally using **Ollama**.

---

## ✨ Why Gmail Ollama Cleanup Agent?

Managing thousands of unread and unwanted emails manually is tedious.

This project combines:

* 🤖 **Ollama** for local AI intent understanding
* 📧 **Gmail API** for mailbox operations
* 🛡️ **Safety validation** before destructive actions
* 👀 **Preview before cleanup**
* ✅ **Explicit confirmation**
* 🧹 **Bulk cleanup with Gmail pagination**
* 🧪 **Automated tests**
* 🔐 **OAuth-based Gmail access**

The goal is simple:

> **Talk to your inbox instead of manually building Gmail search queries.**

---

## 🎯 Example

Instead of manually writing:

```text
is:unread older_than:30d -is:starred
```

you can simply say:

```text
delete unread emails older than 30 days except starred emails
```

The application uses Ollama to understand the request and converts it into a validated Gmail query.

```text
Natural Language
       │
       ▼
    Ollama
       │
       ▼
Structured Intent
       │
       ▼
Safety Validation
       │
       ▼
Gmail Search
       │
       ▼
Preview
       │
       ▼
Explicit Confirmation
       │
       ▼
Move to Gmail Trash
```

---

# 🚀 Features

### 🤖 Local AI with Ollama

Currently uses Ollama for local natural-language intent parsing.

Default model:

```text
llama3.2
```

You can change the model through `.env`.

---

### 📧 Gmail Integration

Uses the official Gmail API with OAuth 2.0.

The application can:

* Search Gmail messages
* Read message metadata
* Preview matching messages
* Move messages to Gmail Trash

---

### 🧹 Natural-Language Cleanup

Examples:

```text
show unread emails
```

```text
delete unread emails
```

```text
delete unread emails older than 30 days
```

```text
delete unread emails older than 90 days except starred
```

```text
delete unread promotional emails older than 30 days
```

---

### 🔎 Preview Before Cleanup

Before a destructive operation, the application displays:

```text
Action: trash
Reason: User request
Gmail query: is:unread older_than:30d
Matching messages: 428

Preview:

- Sep 10 | newsletter@example.com | Weekly Newsletter
- Sep 05 | marketing@example.com | Special Offer
- Aug 29 | updates@example.com | Product Update
...
```

You can review what will be affected before confirming.

---

### 🛡️ Safety First

This project intentionally does **not** permanently delete Gmail messages.

The `trash` action means:

```text
Gmail Inbox
     │
     ▼
Gmail Trash
```

It does **not** use Gmail's permanent-delete operation.

Additionally:

* Cleanup queries must contain `is:unread`
* Unsupported actions are rejected
* Dangerous Gmail query patterns are blocked
* Destructive operations require explicit `YES`
* `DRY_RUN=true` can be used for safe testing

---

### 📦 Bulk Cleanup

The application supports Gmail API pagination.

If you have:

```text
4,327 unread emails
```

the application doesn't stop at the first 100.

It retrieves matching messages across multiple Gmail API pages and processes the cleanup in batches.

From the user's perspective:

```text
delete unread emails
        ↓
4,327 matches
        ↓
one confirmation
        ↓
4,327 moved to Trash
```

---

# 🏗️ Architecture

```text
┌──────────────────────────────┐
│            User              │
│ "delete unread emails"       │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│          Ollama              │
│        llama3.2              │
│      Local LLM inference     │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│      Intent Parser           │
│                              │
│ action                       │
│ gmail_query                  │
│ reason                       │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│       Safety Validator       │
│                              │
│ • Allowed actions            │
│ • is:unread requirement      │
│ • Query safety checks        │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│          Gmail API           │
│                              │
│ Search → Preview → Trash     │
└──────────────────────────────┘
```

---

# 📂 Project Structure

```text
gmail_ollama_cleanup_agent/
│
├── agent/
│   ├── __init__.py
│   └── gmail_agent.py
│
├── gmail/
│   ├── __init__.py
│   └── client.py
│
├── llm/
│   ├── __init__.py
│   ├── ollama_client.py
│   └── parser.py
│
├── credentials/
│   └── .gitkeep
│
├── tests/
│   ├── __init__.py
│   └── test_parser.py
│
├── .env.example
├── .gitignore
├── config.py
├── main.py
├── requirements.txt
└── README.md
```

---

# 💻 Requirements

Before starting, install:

* Python **3.11+**
* Gmail account
* Google Cloud project
* Gmail API enabled
* Ollama
* An Ollama model such as `llama3.2`

Recommended:

```text
Python 3.13+
```

---

# 🦙 Install Ollama

Download and install Ollama:

👉 https://ollama.com/

Verify:

```bash
ollama --version
```

Pull the default model:

```bash
ollama pull llama3.2
```

Verify:

```bash
ollama list
```

You should see something similar to:

```text
NAME       SIZE
llama3.2   ...
```

Make sure Ollama is running:

```bash
ollama serve
```

If Ollama is already running as a background service, you don't need to start it manually.

---

# 📥 Clone the Repository

```bash
git clone https://github.com/raushan-raj-ai-engineer/gmail_ollama_cleanup_agent.git
```

```bash
cd gmail_ollama_cleanup_agent
```

---

# 🐍 Create a Virtual Environment

macOS/Linux:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Windows:

```powershell
python -m venv .venv
```

```powershell
.venv\Scripts\activate
```

---

# 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔐 Configure Gmail OAuth

This application uses Gmail OAuth 2.0.

## 1. Create a Google Cloud Project

Open:

👉 https://console.cloud.google.com/

Create a new project.

Example:

```text
Gmail Ollama Cleanup Agent
```

---

## 2. Enable Gmail API

In Google Cloud Console:

```text
APIs & Services
      ↓
Library
      ↓
Gmail API
      ↓
Enable
```

---

## 3. Configure OAuth Consent Screen

Go to:

```text
APIs & Services
      ↓
OAuth consent screen
```

Configure the application.

For local development, you can use an external/testing configuration depending on your Google Cloud setup.

---

## 4. Create OAuth Client

Go to:

```text
APIs & Services
      ↓
Credentials
      ↓
Create Credentials
      ↓
OAuth Client ID
```

Choose:

```text
Desktop app
```

Download the credentials JSON.

Rename it:

```text
credentials.json
```

Place it here:

```text
credentials/credentials.json
```

Your structure should be:

```text
credentials/
├── credentials.json
└── token.json
```

### ⚠️ IMPORTANT

Never commit either file to GitHub.

```text
credentials.json ❌
token.json       ❌
```

They are intentionally excluded by `.gitignore`.

---

# ⚙️ Configure Environment

Create your local `.env`:

```bash
cp .env.example .env
```

Example:

```env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2

GMAIL_CREDENTIALS_FILE=credentials/credentials.json
GMAIL_TOKEN_FILE=credentials/token.json

DRY_RUN=true
MAX_MESSAGES_PER_RUN=100
```

---

# 🧪 First Run — SAFE MODE

For your first run, keep:

```env
DRY_RUN=true
```

Start the application:

```bash
python main.py
```

You should see:

```text
Gmail + Ollama Cleanup Agent
Type 'exit' to quit.

You:
```

Try:

```text
show unread emails
```

The application will authenticate with Google the first time.

Your browser will open for OAuth authorization.

After successful authorization, a token is stored locally:

```text
credentials/token.json
```

Future runs normally reuse the token.

---

# 💬 Supported Commands

## Show unread emails

```text
show unread emails
```

Example:

```text
Action: preview
Gmail query: is:unread
Matching messages: 100

Preview:
...
```

---

## Delete unread emails

```text
delete unread emails
```

This means:

```text
is:unread
```

The application previews the matches first.

---

## Delete old unread emails

```text
delete unread emails older than 30 days
```

Converted to:

```text
is:unread older_than:30d
```

---

## Exclude starred messages

```text
delete unread emails older than 90 days except starred
```

Converted to:

```text
is:unread older_than:90d -is:starred
```

---

## Promotional emails

```text
delete unread promotional emails older than 30 days
```

The model can identify:

```text
category:promotions
```

along with:

```text
is:unread
older_than:30d
```

---

# ⚠️ Enabling Actual Cleanup

The default configuration is:

```env
DRY_RUN=true
```

This means:

```text
Nothing is moved to Trash.
```

After you have verified the application behaves as expected, you can change:

```env
DRY_RUN=false
```

Then:

```bash
python main.py
```

For example:

```text
You: delete unread emails
```

The application will display the matching count and preview.

You will then see:

```text
Move ALL 1247 matching message(s) to Trash?
Type YES to confirm:
```

Only entering:

```text
YES
```

will execute the cleanup.

Anything else cancels the operation.

---

# 🧹 What "Delete" Means

This application deliberately uses:

```text
Move to Gmail Trash
```

instead of permanent deletion.

Therefore:

```text
delete unread emails
```

means:

```text
Unread Email
     ↓
Gmail Trash
```

It does **not** mean:

```text
Permanent deletion
```

This is an intentional safety design decision.

---

# 🔄 Bulk Processing

Gmail API results are paginated.

For example, if there are:

```text
4,327 matching emails
```

the application retrieves them across multiple API pages.

Deletion is then performed in batches:

```text
1000
1000
1000
1000
327
```

This allows a single user command to process large numbers of matching messages while respecting Gmail API batch limits.

---

# 🧪 Run Tests

Run:

```bash
pytest -q
```

Expected result:

```text
3 passed
```

or the number of tests currently included in the repository.

You can also run:

```bash
python -m compileall .
```

---

# 🔐 Security

This project requires Gmail access through OAuth.

The application does **not** ask for your Gmail password.

Sensitive files are local:

```text
credentials/credentials.json
credentials/token.json
.env
```

These files should never be committed to Git.

Before pushing changes, check:

```bash
git status
```

and:

```bash
git ls-files credentials
```

Only this should normally be tracked:

```text
credentials/.gitkeep
```

---

# 🧠 Why Ollama?

The first version intentionally uses Ollama.

Benefits:

* Local inference
* No external LLM API key
* Useful for privacy-focused experimentation
* Easy local development
* No per-request cloud LLM cost
* Model can be changed through configuration

Current provider:

```text
Ollama
```

Current default model:

```text
llama3.2
```

---

# 🛠️ Current Technology Stack

| Component      | Technology               |
| -------------- | ------------------------ |
| Language       | Python                   |
| LLM            | Ollama                   |
| Model          | llama3.2                 |
| Email          | Gmail API                |
| Authentication | Google OAuth 2.0         |
| Configuration  | python-dotenv            |
| Validation     | Custom intent validation |
| Testing        | pytest                   |
| API Client     | google-api-python-client |

---

# 🗺️ Roadmap

The project currently focuses on a **local Ollama-powered Gmail cleanup MVP**.

### ✅ Phase 1 — Current

* [x] Gmail OAuth
* [x] Gmail API integration
* [x] Ollama integration
* [x] Natural-language cleanup requests
* [x] Structured LLM output
* [x] Gmail query validation
* [x] Preview mode
* [x] Dry-run mode
* [x] Explicit destructive-action confirmation
* [x] Gmail pagination
* [x] Bulk Trash operations
* [x] Automated tests

---

### 🚧 Phase 2 — AI Provider Architecture

* [ ] LLM provider abstraction
* [ ] Gemini support
* [ ] OpenAI support
* [ ] Provider configuration
* [ ] Model selection
* [ ] Improved structured intent schema
* [ ] More robust intent validation

---

### 🔮 Phase 3 — Smart Inbox

* [ ] Newsletter detection
* [ ] Promotional email analysis
* [ ] Sender grouping
* [ ] Duplicate email detection
* [ ] Attachment analysis
* [ ] Old email discovery
* [ ] AI-assisted inbox categorization
* [ ] Cleanup recommendations

---

### 🔮 Phase 4 — Web Application

* [ ] Web UI
* [ ] Google Sign-In
* [ ] Gmail account connection
* [ ] Visual cleanup dashboard
* [ ] Search and filtering
* [ ] Cleanup history
* [ ] Audit logs
* [ ] Undo workflows

---

### 🔮 Phase 5 — Automation

* [ ] Scheduled cleanup previews
* [ ] User-defined cleanup rules
* [ ] Recurring inbox analysis
* [ ] Notification system
* [ ] Approval workflows

---

### 🔮 Phase 6 — SaaS

* [ ] Multi-user architecture
* [ ] Secure token storage
* [ ] Usage metering
* [ ] Subscription plans
* [ ] Billing integration
* [ ] Admin dashboard
* [ ] Monitoring
* [ ] Production deployment
* [ ] Privacy controls

---

# 🤝 Contributing

Contributions are welcome.

You can contribute by:

* Reporting bugs
* Suggesting features
* Improving documentation
* Adding tests
* Improving safety validation
* Adding LLM providers
* Improving Gmail integration

Typical workflow:

```bash
git checkout -b feature/my-feature
```

Make your changes:

```bash
git add .
git commit -m "Add my feature"
```

Push:

```bash
git push origin feature/my-feature
```

Then open a Pull Request.

---

# ⚠️ Disclaimer

This is an open-source project intended for experimentation and personal use.

Review the Gmail permissions requested by the application and understand what actions it performs before authorizing access.

Always test with:

```env
DRY_RUN=true
```

before enabling destructive operations.

---

# ⭐ Support the Project

If you find this project useful:

⭐ Star the repository

🐛 Report issues

💡 Suggest improvements

🤝 Contribute

📢 Share it with other developers interested in local AI and automation.

---

# 📜 License

This project is released under the **MIT License**.

See [`LICENSE`](LICENSE) for details.

---

## 🚀 What's Next?

This project starts with a simple idea:

> **Can we make Gmail cleanup conversational while keeping the AI local and the actual mailbox operations deterministic and safe?**

The current answer is the Ollama-powered CLI.

The long-term direction is a complete AI-powered inbox management platform.

**Local AI → Smart Cleanup → Web App → Automation → SaaS**

⭐ **Star the repository and follow the journey.**
