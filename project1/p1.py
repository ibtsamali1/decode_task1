def chatbot():
    print("=" * 50)
    print("🤖 Rule-Based AI Chatbot")
    print("Type 'bye' or 'exit' to quit.")
    print("=" * 50)

    while True:
        user = input("\nYou: ").lower().strip()

        if user in ["hi", "hello", "hey"]:
            print("Bot: Hello! How can I help you today?")

        elif user == "how are you":
            print("Bot: I'm doing great! Thanks for asking.")

        elif user == "your name":
            print("Bot: I am DecodeBot, a rule-based AI chatbot.")

        elif user == "what can you do":
            print("Bot: I can answer basic predefined questions.")

        elif user == "python":
            print("Bot: Python is a popular programming language for AI and automation.")

        elif user == "ai":
            print("Bot: AI stands for Artificial Intelligence.")

        elif user == "help":
            print("Bot: Try asking:")
            print("- hello")
            print("- how are you")
            print("- your name")
            print("- python")
            print("- ai")
            print("- time")
            print("- date")
            print("- bye")

        elif user == "time":
            from datetime import datetime
            print("Bot:", datetime.now().strftime("Current Time: %H:%M:%S"))

        elif user == "date":
            from datetime import datetime
            print("Bot:", datetime.now().strftime("Today's Date: %d-%m-%Y"))

        elif user in ["bye", "exit", "quit"]:
            print("Bot: Goodbye! Have a nice day.")
            break

        else:
            print("Bot: Sorry, I don't understand that.")

if __name__ == "__main__":
    chatbot()