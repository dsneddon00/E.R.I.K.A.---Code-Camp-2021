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
    "Hi",
    "Hello, my name is Erika.",
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
            },
            

        ]
    )
    return chatbot

def train(bot):
    trainer = ListTrainer(bot)
    trainer.train([
        "Hi",
        "Hello, my name is Erika. How are you feeling today?",
        "I am doing fine",
        "Is everything going well in your life?"    
    ])
    trainer.train([
        "Hello",
        "Hello, my name is Erika. How are you feeling today? Neutral,good,bad?" ,
    ])
    trainer.train([
        "good",
        "Great. Is everything going well in your life?"
    ])
    trainer.train([
        "Bad",
        "I'm sorry to hear. Is everything going well in your life?"
    ])
    trainer.train([
        "neutral",
        "Is everything going well in your life?"
    ])
    trainer.train([
        "It is not great",
        "I am your Empathecticly Reciprocating Intelligent Konnection Agent, or Erika for short. Remember, I am not a counselor, but I will do my best to make you feel better.If you are in immediate danger, please call 911 or reach out to a local helpline here: https://www.nami.org/help. If you need professional help reach out to a local helpline here: https://www.nami.org/help. Would you like some tips to relax and reconnect with your body and mind?",
        "Yes",
        "Great to hear. One of the first ways to be more connected with yourself to focus on your breath. Take a long, deep breath... As you breath, let your mind be free of repetitive or negative thoughts. How do you feel? A little better or not better",
    ])
    trainer.train([
        'Not better',
        "I am sorry that didn't help. Let's try to do another exercise and see if it is benefical for you. It's called the Body scan. This technique is to help relax the muscles in your body. Continue your breath focus and go from muscle to muscle on your body releasing physical tension in that muscle. It's all about being aware of the mind and body connection. After let me know, Have you released any tension in the body? Less tension or the same tension",
    ])
    trainer.train([
        "A little better",
        "Good job. Let's try another exercise. It's called the Body scan. This technique is to help relax the muscles in your body. Continue your breath focus and go from muscle to muscle on your body releasing physical tension in that muscle. It's all about being aware of the mind and body connection. After let me know, Have you released any tension in the body? Less tension or the same tension",
    ])
    trainer.train([
        "Same tension", 
        "I'm sorry to hear that. Let's try another technique and see if it helps. It's called guided imagery. I would like you to close your eyes and think of a calm place or a place you would find peace. Think of a scene that you personally relate to and let your mind wander in that place. Let me know how are you feeling after.. I'll wait here. Better, worse, same?",
    ])
    trainer.train([
        "Less tension",
        "That is a very important step leading to the the guided imagery. I would like you to close your eyes and think of a calm place or a place you would find peace. Think of a scene that you personally relate to and let your mind wander in that place. Let me know how are you feeling after.. I'll wait here. Better, worse, same?"
    ])
    trainer.train([
        "Better",
        "Glad to hear, I'm here to help. So do have days that you feel depressed, anxious, or both? "
    ])
    trainer.train([
        "Worse",
        "I'm sorry. Let's try to improve your mood. Do have days that you feel depressed, anxious, or both? "
    ])
    trainer.train([
        "Same",
        "It's okay to feel about the same. But let's try to dig a little deeper to understand what can help. Do have days that you feel depressed, anxious, or both? "
    ]) 
    trainer.train([
        "Depressed",
        "There's a lot of people that deal with depression. You are not alone. You can get through this and find ways to cope. Let's talk about it.\n  Are you active or not active"
    ])

    trainer.train([
        "Active",
        "Great. Working out or being active in general is so good for coping with depression. Try new workout plans, plan a hike to a new place, pick a new active hobby like mountain biking, or anything that might interest you.\n "
    ])
    trainer.train([
        "Not active",
    ])
    trainer.train([
        "Anxious",
        "There's a lot of people that deal with anxiety. You are not alone."
    ])
    trainer.train([
        "Both",
        "Theres a lot people that deal with depression and anxiety. You are not alone."
    ])
    trainer.train([
        "Bye",
        "Thanks for talking. If you need professional help reach out to a local helpline here: https://www.nami.org/help. You are not alone. Come back anytime"
    ])
  

  
 

def inputHandler(bot):
    # find a way to send the mode up to the server
    mode = "light"
    while True:
        try:
            response = bot.get_response(input("Input your message here: "))
            print(response)
            if(str(response) == "Changing to dark mode" and mode != "dark"):
                mode = "dark"
            elif(str(response) == "Changing to light mode" and mode != "light"):
                # the bot is confusing light and dark mode
                mode = "light"

        except(KeyboardInterrupt, EOFError, SystemExit):
            break

def run():
    bot = generateChatBot()
    train(bot)
    inputHandler(bot)

# run()

################################################

class Robot:
    def __init__(self, userID=-1, mode="light"):
        self.robot = generateChatBot()
        train(self.robot)
        self.userID = userID
        self.mode = mode
    
    def chat(self, text):
        response = self.robot.get_response(text)
        # print(response)

        if(str(response) == "Changing to dark mode" and self.mode != "dark"):
                self.mode = "dark"
        elif(str(response) == "Changing to light mode" and self.mode != "light"):
                # the bot is confusing light and dark mode
                self.mode = "light"

        return str(response)


####################################################
