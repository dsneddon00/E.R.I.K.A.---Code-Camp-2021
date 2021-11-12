#! /usr/bin/env python3
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import logging

logger = logging.getLogger()
logger.setLevel(logging.CRITICAL)

# Empatheticly Reciprocating Intelligent Konnection Agent
#chatbot = ChatBot("ERIKA")


chatbot = ChatBot("Erika",
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
    database_uri="sqlite:///erikaTraining.sqlite3",
    logic_adapter=["chatterbot.logic.BestMatch"])

conversation = [
    "Hello.",
    "My name is Erika.",
    "How are you feeling today?",
    "I am well, thank you for asking.",
    "Is everything going well in your life?",
    "I am your Empathecticly Reciprocating Intelligent Konnection Agent, or Erika for short."
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
