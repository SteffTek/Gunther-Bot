import time
import threading
import pymongo

from tools import dc_integration, commands, learning, ownLogger, banManager, settings, spamProtect, badWords

class commandManager:
    def __init__(self, dc_bot, main):
        self.dc_bot = dc_bot
        self.main = main
        self.__mongodb = pymongo.MongoClient(settings.mongo_db_database)
        self.__mydb = self.__mongodb["justbot"]
        self.__mycol = self.__mydb["statements"]

    def command(self, x):
        argsLength = len(x.split(" "))
        command = x

        if argsLength > 0:
            args = x.split(" ")
            command = args[0].lower()
            args.pop(0)
            argsLength = len(args)


        if argsLength > 0:
            if command.lower() == "ban":
                if self.main.banManager.banID(args[0]) == True:
                    print(args[0] + " successfully banned!")
                    return args[0] + " successfully banned!"
                else:
                    print(args[0] + " already banned!")
                    return args[0] + " already banned!"

            if command.lower() == "unban":
                try:
                    if self.main.banManager.unBanID(args[0]) == True:
                        print(args[0] + " successfully unbanned!")
                        return args[0] + " successfully unbanned!"
                    else:
                        print(args[0] + " not banned!")
                        return args[0] + " not banned!"
                except:
                    print("An error occurred!")
                    return "UserID not banned!"

            if command.lower() == "banword":
                if self.main.badWords.ban(args[0]) == True:
                    print("Word " + args[0] + " successfully banned!")
                    return "Word " + args[0] + " successfully banned!"
                else:
                    print(args[0] + " already banned!")
                    return args[0] + " already banned!"

            if command.lower() == "unbanword":
                try:
                    if self.main.badWords.unBan(args[0]) == True:
                        print("Word " + args[0] + " successfully unbanned!")
                        return "Word " + args[0] + " successfully unbanned!"
                    else:
                        print("Word " + args[0] + " not banned!")
                        return "Word " + args[0] + " not banned!"
                except:
                    print("An error occurred!")
                    return "Word was not banned!"

            if command.lower() == "remove":
                searchString = ""

                for i in args:
                    searchString = searchString + " " + i

                searchString = searchString.strip()

                query = { "text": searchString}
                query2 = {"in_response_to": searchString}
                x = self.__mycol.delete_many(query)
                print("Deleted Text", x.deleted_count)
                xx = self.__mycol.delete_many(query2)
                print("Deleted In_response", xx.deleted_count)

                count = x.deleted_count + xx.deleted_count

                return "Deleted " + str(count) + " entries!"

        return None