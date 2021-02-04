from . import settings, dc_integration

from random import choice
import time
import discord

class fun:

    def __init__(self, bot):
        print("Initialized F.U.N.")
        self.__bot = bot
        self.__modrole = settings.mod_role # BOT PERMS bei nero

    async def onMessage(self, message, string):
        msg = string.lower()
        author = message.author

        # Admin Commands
        if self.__bot.checkForModRole(author.roles):
            if msg.startswith("was machst du hier"):
                msg = '{0.author.mention}: ' + "Also ich bin nur hier, weil ich euch alle so lieb hab 😊"
                msg = msg.format(message)
                await message.channel.send(msg)
                return True
            if msg.startswith("wer hat dir das beigebracht"):
                msg = '{0.author.mention}: ' + "Das war garantiert nicht Lyi, nein nein sie würde so etwas NIEEEEMAAALS machen ich schwööööreeee! 😉"
                msg = msg.format(message)
                await message.channel.send(msg)
                return True

        # Normale Commands
        if msg.startswith("schalt dich ab"):
            msg = '{0.author.mention}: ' + "Ok ._."
            msg = msg.format(message)
            await message.channel.send(msg)

            # REBOOT SCREEN
            new_msg = await message.channel.send("Beep boop...")
            time.sleep(0.5)
            await new_msg.edit(content="Beep boop... R")
            time.sleep(0.1)
            await new_msg.edit(content="Beep boop... Re")
            time.sleep(0.1)
            await new_msg.edit(content="Beep boop... Reb")
            time.sleep(0.1)
            await new_msg.edit(content="Beep boop... Rebo")
            time.sleep(0.1)
            await new_msg.edit(content="Beep boop... Reboo")
            time.sleep(0.1)
            await new_msg.edit(content="Beep boop... Reboot")
            time.sleep(0.1)
            await new_msg.edit(content="Beep boop... Rebooti")
            time.sleep(0.1)
            await new_msg.edit(content="Beep boop... Rebootin")
            time.sleep(0.1)
            await new_msg.edit(content="Beep boop... Rebooting...")
            time.sleep(2)
            await new_msg.edit(content="Beep boop... Reboot complete!")
            return True
        if msg.startswith("was machst du hier"):
            msg = '{0.author.mention}: ' + "Um ehrlich zu sein, die Admins zwingen mich..."
            msg = msg.format(message)
            await message.channel.send(msg)
            return True
        if msg.startswith("wer ist der beste nutzer") or msg.startswith("wer ist der beste"):
            msg = '{0.author.mention}: ' + "Hmm lass mich kurz schauen..."
            msg = msg.format(message)
            await message.channel.send(msg)
            time.sleep(3)

            new_msg = await message.channel.send("AH ICH HABS! Es ist...")
            time.sleep(1)
            await new_msg.edit(content="X7DLdiAkDLie")
            time.sleep(0.1)
            await new_msg.edit(content="LJSDf8§NÖJd")
            time.sleep(0.1)
            await new_msg.edit(content="§)JSLF(SFLJF§")
            time.sleep(0.1)
            await new_msg.edit(content="MJÖLJFU WWEF")
            time.sleep(0.1)
            await new_msg.edit(content="EWFD§IJFOW")
            time.sleep(0.1)
            await new_msg.edit(content="EWFDFSIFJWE§F")
            time.sleep(0.1)
            await new_msg.edit(content="DFSEFW§OF")
            time.sleep(0.1)
            await new_msg.edit(content="__**Message corrupted. Please try again later.**__")
            return True
        if msg.startswith("wer ist dein lieblingsnutzer") or msg.startswith("wer ist dein liebling"):
            # Random User
            user = choice(message.channel.guild.members)

            if user is None:
                return False

            msg = '{0.author.mention}: ' + "Mein Lieblings-Nutzer ist " + user.nick + " :3"
            msg = msg.format(message)
            await message.channel.send(msg)
            return True

        if msg.startswith("help"):
            msg = '{0.author.mention}: ' + "Vielleicht hilft dir das: \n\n Wenn ich mit 💢 reagiere, bin ich mir nicht sicher ob meine Antwort korrekt ist. \n Bei einem ❌ wurde ein verbotenes Wort verwendet. \n Und bei ⚠️ weiß ich einfach nicht, was ich antworten soll ¯\_(ツ)_/¯"
            msg = msg.format(message)
            await message.channel.send(msg)
            return True
        return False