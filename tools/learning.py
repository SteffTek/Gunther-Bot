import threading
import time

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer

class learning:

    def __init__ (self, main, bot):
        self.__main = main
        self.__bot = bot

        self.__list_trainer = ListTrainer(self.__bot)

        self.__todo = []

        self.initialized = False

        #Threading
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def stopThread(self):
        self.initialized = False

    # Add an Item
    def addToList(self, string):
        self.__todo.append(string)

    # Run Trainer
    def run(self):
        self.initialized = True

        for item in self.__todo:
            self.__list_trainer.train(item)

        self.__todo.clear()

        time.sleep(30)

        while self.initialized:
            self.run()