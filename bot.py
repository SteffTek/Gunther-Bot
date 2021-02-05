import os

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.comparisons import LevenshteinDistance

import logging, threading

from tools import dc_integration, commands, learning, ownLogger, banManager, settings, spamProtect, badWords, fun

logger = logging.getLogger()
logger.setLevel(logging.CRITICAL)

class __main__:
    def __init__ (self):
        print("Botter Initialized!")

        ###############UTILS################
        try:
            os.makedirs("user_audio")
        except FileExistsError as e:
            print("Dir user_audio initialized...")

        ###############BOTCREATION################

        should_learn = not settings.enable_learning
        print("Is learning disabled: " + str(should_learn))

        self.__my_bot = ChatBot(name='PyBot',
            read_only=should_learn,
            storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
            database_uri=settings.mongo_db_database,
            logic_adapters=[
                {
                    "import_path": "chatterbot.logic.BestMatch",
                    "statement_comparison_function":"chatterbot.comparisons.LevenshteinDistance"
                }
            ]
        )

        #CORPUS TRAINER EXAMPLE
        trainer = ChatterBotCorpusTrainer(self.__my_bot)
        #trainer.train(
            #"chatterbot.corpus.german"
        #)

        self.logger = ownLogger.logger()
        ################DISCORD##################

        """
            Startet neuen Thread in der Bot-Class
        """
        self.banManager = banManager.banManager()
        self.badWords = badWords.badWords()
        self.spamProtect = spamProtect.spamProtect(self)

        self.__TOKEN = settings.discord_token
        self.dc_bot = dc_integration.dc_bot(self, self.__my_bot, self.__TOKEN)

        ################LEARNING#################
        """
            This is literally never executed
            and just here for debugging purposes.
        """
        ##self.learning = learning.learning(self, self.__my_bot)


main = __main__()
