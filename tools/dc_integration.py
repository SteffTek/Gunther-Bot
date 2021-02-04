import discord
import threading
import asyncio
import pickle

from urllib.parse import urlparse
from tools import commands, settings, fun, wss

import re

class dc_bot:
    def __init__ (self, main, bot, token):
        self.main = main
        self.__token = token
        self.client = discord.Client()
        self.bot = bot
        self.__commands = commands.commandManager(self, main)
        self.__fun = fun.fun(self)

        self.__chatchannel = settings.chatchannel
        self.__logchannel = settings.logchannel
        self.__modrole = settings.mod_role
        self.__prefix = settings.discord_command_prefix

        self.initialized = False

        policy = asyncio.get_event_loop_policy()
        policy._loop_factory = asyncio.SelectorEventLoop

        self.__wss = wss.WSS(self)

        self.emojiMap = {}
        self.__loadEmojiMap()

        self.run()

    async def formatMessage(self, message, stripNames = False):
        string = str(message.content)

        # Send to Spam
        self.client.loop.create_task(self.main.spamProtect.onMessage(message))

        #print(str(message.author.id) + ";" + message.author.name + " (" + message.channel.guild.name + "|" + message.channel.name + "): " + message.content)
        if isinstance(message.channel, discord.DMChannel):
            self.main.logger.writeLog(str(message.author.id) + ";" + message.author.name + " (PRIVAT CHAT): " + message.content)
        else:
            self.main.logger.writeLog(str(message.author.id) + ";" + message.author.name + " (" + message.channel.guild.name + "|" + message.channel.name + "): " + message.content)

        # Check if Mass Mention, if - Ignore
        if message.mention_everyone:
            return None

        # Check for URL
        if len(self.__checkForURL(string)) > 0:
            return None


        # Delete @BOT Mention
        uuid = str(self.client.user.id)
        string = string.replace("<@!" + uuid + ">","")
        string = string.replace("<@" + uuid + ">","")

        # Custom Emoji to Tag //NOT ANIMATED
        custom_emojis = re.findall(r'<:\w*:\d*>', string)
        tag_emojis = [str(e.split(':')[1].replace('>', '')) for e in custom_emojis]

        # Custom Emoji to Tag //ANIMATED
        custom_animated_emojis = re.findall(r'<a:\w*:\d*>', string)
        animated_emojis = [str(e.split(':')[1].replace('>', '')) for e in custom_animated_emojis]

        tag_emojis = tag_emojis + animated_emojis
        custom_emojis = custom_emojis + custom_animated_emojis

        emoji_count = 0
        for emoji in tag_emojis:

            emoji_code = custom_emojis[emoji_count]

            emoji_id = re.findall(r':\w*:\d*>', emoji_code)
            emoji_id = [str(e.split(':')[2].replace('>', '')) for e in emoji_id][0]

            if not self.client.get_emoji(int(emoji_id)) is None:
                string = string.replace(emoji_code, ":" + emoji + ":")

                # Set emoji map
                if not emoji in self.emojiMap:
                    self.emojiMap[emoji] = emoji_code
                    self.__saveEmojiMap()
                    print("Saved Emoji Map, New Emoji: " + emoji)

            else:
                string = string.replace(emoji_code, "")

            emoji_count = emoji_count + 1

        # Replace Mentions with Names
        for member in message.mentions:
            # Get Member ID
            memberID = str(member.id)

            if stripNames == True:
                # Strip names if normal learning
                string = string.replace("<@!" + memberID + ">", "")
            else:
                # Replace Mention with Name
                string = string.replace("<@!" + memberID + ">", member.name)
                string = string.replace("<@" + memberID + ">", member.name)

        # Strip leading spaces
        string = string.strip()
        if len(string.replace(" ","")) < 2:
            return None

        #FUN CHECK
        isFun = await self.__fun.onMessage(message, string)
        if isFun == True:
            return {"fun":True}

        # Check if Bot Command (Starts with ".", "!", "?", "-")
        botPrefixes = [".","!","?","-","+","~"]
        for prefix in botPrefixes:
            if string.startswith(prefix):
                return None

        # Bad Word Check
        bannedWords = self.main.badWords.containsBad(string)
        if len(bannedWords) > 0:
            return {"err": "banned.word", "words": bannedWords}

        return string

    async def sendResponse(self, string, message, ownChannel = True, isPrivate = False):
        print("DC > ", string)
        statement = self.bot.get_response(string)
        print("DC < ", str(statement), "; Confidence: " , statement.confidence)

        if statement.confidence < 0.2 and ownChannel == False:
            return

        msg = str(statement)

        #debugging only
        #msg = str("Du hast meinen Satz kopiert? <:thinking_ban:742838457734266981> Du bist ja schlau :yikesbrowtf:")
        #msg = string

        # Load Emoji Map
        tag_emojis = re.findall(r'(?<!<):\w*:', msg)
        tag_emojis = list(dict.fromkeys(tag_emojis)) # REMOVE DOUBLE EMOTES
        emoji_count = 0
        for emoji in tag_emojis:
            msg = msg.replace(emoji, self.emojiMap[emoji.replace(":","")])
            emoji_count = emoji_count + 1

        if isPrivate == False and ownChannel == True:
            msg = '{0.author.mention}: ' + msg

        msg = msg.format(message)

        sent_msg = await message.channel.send(msg)

        if statement.confidence < 0.2:
            await sent_msg.add_reaction("💢")

    def __checkForURL(self, string):
        # findall() has been used
        # with valid conditions for urls in string
        #url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+] |[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string)
        url = re.findall('(?P<url>https?://[^\s]+)', string)

        if url is not None:
            if len(url) == 1:
                # Überprüfen ob URL in Whitelist
                parsed_uri = urlparse(url[0])
                result = '{uri.netloc}'.format(uri=parsed_uri)

                if result.lower() in settings.whitelisted_websites:
                    return []

        return url

    def checkForModRole(self, roles):
        for i in roles:
            if str(i.id) == self.__modrole:
                return True

        return False

    def __saveEmojiMap(self):
        with open('Config/EmojiMap.pkl', 'wb') as f:
            pickle.dump(self.emojiMap, f, pickle.HIGHEST_PROTOCOL)

    def __loadEmojiMap(self):
        try:
            with open('Config/EmojiMap.pkl', 'rb') as f:
                self.emojiMap = pickle.load(f)
                print("Loaded Emoji Map:")
                print(str(self.emojiMap))
        except FileNotFoundError as e:
            self.__saveEmojiMap()
            self.__loadEmojiMap()

    def run(self):
        asyncio.get_event_loop()

        #MSG Event
        @self.client.event
        async def on_message(message):
            # Check if normal message
            if not message.type == discord.MessageType.default:
                return

            # Don't respond on own messages
            if message.author == self.client.user:
                return

            # Is Banned? (Fucking Hurensohn)
            if self.main.banManager.isBanned(message.author.name):
                return

            # Banned IDs too!
            if self.main.banManager.isBanned(str(message.author.id)):
                return

            # Ignore Bots
            if message.author.bot == True:
                return

            # Private Chat
            if isinstance(message.channel, discord.DMChannel):

                # Disabled weil wegen Nero
                return

                # Get Message
                formattedMessage = self.formatMessage(message)
                if formattedMessage is None:
                    return

                # Formatted Message is Valid
                #await message.channel.send(self.getResponse(formattedMessage, message, True))
                self.client.loop.create_task(self.sendResponse(formattedMessage, message, True))
                return

            # Only respond in right channel
            if message.channel.id == self.__chatchannel:

                # Check for command
                if str(message.content).startswith(self.__prefix):
                    # Send to Commandmanager if modrole in Roles
                    if self.checkForModRole(message.author.roles) == True:
                        print(message.author.name + ": " + message.content)
                        string = str(message.content)[len(self.__prefix):]
                        respone = self.__commands.command(string)

                        if respone is None:
                            return

                        msg = '{0.author.mention}: ' + respone
                        msg = msg.format(message)
                        await message.channel.send(msg)
                        await message.delete()
                    # exit
                    return


                # Don't Respond if not Mentioned
                if not self.client.user in message.mentions:
                    # Learn from Message
                    #self.main.learning.addToList(formattedMessage)
                    return

                # Get Message
                formattedMessage = await self.formatMessage(message)
                if formattedMessage is None:
                    await message.add_reaction("⚠️")
                    return

                if isinstance(formattedMessage, dict):
                    if formattedMessage.get("err") == "banned.word":
                        await message.add_reaction("❌")
                        await message.channel.guild.get_channel(self.__logchannel).send(message.author.name + "#" + message.author.discriminator + " used banned word in message: \nWords: " + str(formattedMessage.get("words")) + "\n\nMessage:" + message.content)
                    if formattedMessage.get("fun") == True:
                        print("Es wurde F.U.N. ausgeführt!")
                    return

                # Formatted Message is Valid
                #await message.channel.send(self.getResponse(formattedMessage, message))
                self.client.loop.create_task(self.sendResponse(formattedMessage, message, ownChannel=True))
                return

            else:
                if str(message.channel.id) in settings.whitelisted_channels:
                    formattedMessage = await self.formatMessage(message)
                    if formattedMessage is None:
                        return

                    if isinstance(formattedMessage, dict):
                        return

                    if not self.client.user in message.mentions:
                        self.client.loop.create_task(self.sendResponse(formattedMessage, message, ownChannel=False))
                    else:
                        self.client.loop.create_task(self.sendResponse(formattedMessage, message, ownChannel=True))


            if not self.client.user in message.mentions:
                # Give Message to Learn
                # Lernen hat nicht geklappt, viele Random buchstaben.. :(
                return

                # Get Message
                #formattedMessage = self.formatMessage(message, True)
                #if formattedMessage is None:
                    #return

                # Formatted Message is Valid
                #self.main.learning.addToList(formattedMessage)

        #Ready Event
        @self.client.event
        async def on_ready():
            print('------')
            print('Logged in as')
            print(self.client.user.name)
            print(self.client.user.id)
            print('------')
            self.initialized = True

        #Login Into Client
        self.client.run(self.__token)