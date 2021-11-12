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

# CONSTANTS
DEFAULT_RESPONSE_SET = [
    "Hello.",
    "My name is Erika.",
    "How are you feeling today?",
    "I am well, thank you for asking.",
    "Is everything going well in your life?",
    "I am your Empathecticly Reciprocating Intelligent Konnection Agent, or Erika for short.",
    "Remember, I am not a counselor, but I will do my best to make you feel better.",
    "If you are in immediate danger, please call 911 or reach out to a local helpline here: https://www.nami.org/help",
    "If you need professional help reach out to a local helpline here: https://www.nami.org/help",
    "I would be happy to change it to dark mode, give me a second...",
    "Changing to dark mode",
    #"Changing to light mode"
]

def generateChatBot():

    chatbot = ChatBot("Erika",
        storage_adapter="chatterbot.storage.SQLStorageAdapter",
        database_uri="sqlite:///erikaTraining.sqlite3",
        preprocessors=[
            "chatterbot.preprocessors.clean_whitespace"
        ],
        logic_adapters=[
            {
                "import_path": "chatterbot.logic.BestMatch",
                "default_response": "I am sorry, but I do not understand what you are saying.",
                "maximum_similarity_threshold": 0.90
            }

        ]
    )
    return chatbot

def train(bot, responses):
    trainer = ListTrainer(bot)

    trainer.train(responses)

def inputHandler(bot):
    # find a way to send the mode up to the server
    mode = "light"
    while True:
        try:
            response = bot.get_response(input("Input your message here: "))
            print(response)
            if(str(response) == "Changing to dark mode" and mode != "dark"):
                mode = "dark"
            elif(str(response) == "Changing to light mode" and mode != "ligth"):
                # the bot is confusing light and dark mode
                mode = "light"

        except(KeyboardInterrupt, EOFError, SystemExit):
            break

def run():
    bot = generateChatBot()
    train(bot, DEFAULT_RESPONSE_SET)
    inputHandler(bot)

run()
