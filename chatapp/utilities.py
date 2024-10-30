message_responses = {
    "Hello": "Hi! What can I do for you today?",
    "What is your name?": "You can call me your virtual assistant!",
    "What can you do?" : "I can help you with general questions, provide information, and assist with common issues.",
    "Tell me a joke." : "Why did the computer break up with the printer? Because it felt they weren't on the same page!"
}

def chat_response(message):
    try:
        response = message_responses[message]
        
    except Exception:
        response =  "I am not sure how to respond to that!"
   
    return response