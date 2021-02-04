import os

class banManager:

    def __init__(self):
        self.banned = []
        self.BannedUsers = []

        try:
            os.mkdir("Config")
            f = open("Config/BannedUsers.txt", "w", encoding="utf-8")
            f.close()
            print("Directory /Config Created ")
        except FileExistsError:
            print("Directory /Config already exists")

        self.loadBanned()
        print(self.BannedUsers)

    def saveBanned(self):
        # Load Banned IDs
        with open("Config/BannedUsers.txt", "w", encoding="utf-8") as f:
            for item in self.BannedUsers:
                f.write(item + "\n")

    def loadBanned(self):
        # Load Banned IDs
        with open("Config/BannedUsers.txt", "r", encoding="utf-8") as f:
            line = f.readline()
            while line:
                if len(line) > 0:
                    self.BannedUsers.append(line.rstrip("\n\r"))
                line = f.readline()

    def banID(self, id):
        if id in self.BannedUsers:
            return False

        self.BannedUsers.append(str(id))
        self.saveBanned()
        return True

    def unBanID(self, id):
        if not id in self.BannedUsers:
            return False

        self.BannedUsers.pop(self.BannedUsers.index(str(id)))
        self.saveBanned()
        return True

    def isBanned(self, userdID):
        for item in self.BannedUsers:
            if item == userdID:
                return True
