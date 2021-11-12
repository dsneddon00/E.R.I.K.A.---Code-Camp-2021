#! /usr/bin/env python3
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import logging

logger = logging.getLogger()
logger.setLevel(logging.CRITICAL)

# Empatheticly Reciprocating Intelligent Konnection Agent
#chatbot = ChatBot("ERIKA")

# logic_adapters=["chatterbot.logic.BestMatch",
#"chatterbot.logic.TimeLogicAdapter",
#"chatterbot.logic.MathematicalEvaluation"]

chatbot = ChatBot("Erika",
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
    database_uri="sqlite:///erikaTraining.sqlite3",
    logic_adapters=[
        {
            "import_path": "chatterbot.logic.BestMatch",
            "default_response": "I am sorry, but I do not understand what you are saying.",
            "maximum_similarity_threshold": 0.90
        }
    ]
    )

conversation = [
    "Hello.",
    "My name is Erika.",
    "How are you feeling today?",
    "I am well, thank you for asking.",
    "Is everything going well in your life?",
    "I am your Empathecticly Reciprocating Intelligent Konnection Agent, or Erika for short.",
    "Remember, I am not a counselor, but I will do my best to make you feel better.",
    "If you are in immediate danger, please call 911 or reach out to a local helpline here: https://www.nami.org/help",
    "If you need professional help reach out to a local helpline here: https://www.nami.org/help"
]

trainer = ListTrainer(chatbot)

trainer.train(conversation)

while True:
    try:
        userInput = chatbot.get_response(input("Input your message here: "))
        print(userInput)
    except(KeyboardInterrupt, EOFError, SystemExit):
        break




'''


response = chatbot.get_response("Hello!")

print(response)
'''
