from . import settings
import discord

from tools.info import spamCount

class spamProtect:

    def __init__(self, main):
        self.__tracking = {}
        self.__main = main

    async def onMessage(self, message):
        if not str(message.author.id) in self.__tracking.keys():
            newSpam = spamCount.spamCount()
            self.__tracking[str(message.author.id)] = newSpam

        shouldBan = self.__tracking[str(message.author.id)].update()

        if shouldBan == True:
            self.__main.banManager.banID(str(message.author.id))
            print(message.author.name + " banned for spam!")
            await message.author.send("You got auto-banned from the Chatbot for spamming.")

