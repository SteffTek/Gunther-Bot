import time
from .. import settings

class spamCount:
    def __init__(self):
        #self.__count = 0
        #self.__time = int(round(time.time() * 1000))
        self.__last = []

    def update(self):
        currentTime = time.time()
        self.__last.append(currentTime)

        if len(self.__last) > settings.spam_limit:
            self.__last.pop(0)

            if currentTime - self.__last[0] < settings.spam_time:
                return True

        return False
