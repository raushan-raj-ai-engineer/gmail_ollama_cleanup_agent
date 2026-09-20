from agent.gmail_agent import GmailCleanupAgent

def main() -> None:
    agent = GmailCleanupAgent()
    print("Gmail + Ollama Cleanup Agent")
    print("Type 'exit' to quit.\n")

    while True:
        request = input("You: ").strip()
        if request.lower() in {"exit", "quit"}:
            break
        if not request:
            continue

        try:
            result = agent.handle(request)
            print("\n" + result + "\n")
        except Exception as exc:
            print(f"\nERROR: {exc}\n")

if __name__ == "__main__":
    main()
