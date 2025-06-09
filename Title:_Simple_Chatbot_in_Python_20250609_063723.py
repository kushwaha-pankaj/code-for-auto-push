Title: Simple Chatbot in Python

```python
import random

# Sample responses that the chatbot can use
responses = [
    "That's interesting! Tell me more about it.",
    "I'm not sure I understand, can you elaborate?",
    "Why do you think that is?",
    "How do you feel about that?",
    "That's quite a thought!",
    "Can you explain further?",
    "Oh, really?",
    "What makes you say that?",
    "I see. What happened next?"
]

def chatbot_response(user_input):
    return random.choice(responses)

def main():
    print("Chatbot: Hello! I'm a chatbot. Let's chat.")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit", "goodbye"]:
            print("Chatbot: Goodbye! Have a great day.")
            break
        reply = chatbot_response(user_input)
        print(f"Chatbot: {reply}")

if __name__ == "__main__":
    main()
```