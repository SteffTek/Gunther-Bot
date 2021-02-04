import os

class badWords:

    def __init__(self):
        self.badWords = []

        try:
            os.mkdir("Config")
            f = open("Config/BadWords.txt", "w", encoding="utf-8")
            f.close()
            print("Directory /Config Created ") 
        except FileExistsError:
            print("Directory /Config already exists")

        self.loadWords()
        print(self.badWords)

    def saveWords(self):
        # Load Banned Names
        with open("Config/BadWords.txt", "w", encoding="utf-8") as f:
            for item in self.badWords:
                f.write(item + "\n")

    def loadWords(self):
        # Load Banned Names
        with open("Config/BadWords.txt", "r", encoding="utf-8") as f:
            line = f.readline()
            while line:
                if len(line) > 0:
                    self.badWords.append(line.rstrip("\n\r").lower())
                line = f.readline()

    def ban(self, name):
        name = name.lower()

        if name in self.badWords:
            return False

        self.badWords.append(str(name))
        self.saveWords()
        return True

    def unBan(self, name):
        if not name in self.badWords:
            return False

        self.badWords.pop(self.badWords.index(str(name)))
        self.saveWords()
        return True

    def isBanned(self, nameOrId):
        for item in self.badWords:
            if item == nameOrId:
                return True

    def containsBad(self, string):
        #if any(x in string.lower() for x in self.badWords):
            #res = [i for i in self.badWords if (i in string.lower())]
            #print(str(res))
            # return True
        return [i for i in self.badWords if (i in string.lower())]