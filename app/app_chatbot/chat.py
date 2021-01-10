from .bot import chatbot


while True:
    try:
        user = input("Voce: ")
        response = chatbot.get_response(user)
        
        print("Bot: " + str(response))
        print("Confidence: " + str(response.confidence))
    except (KeyboardInterrupt, EOFError, SystemExit):
        break
