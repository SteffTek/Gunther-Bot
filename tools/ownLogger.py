import os

from datetime import datetime


class logger:

    def __init__(self):
        print("Logger Initialized")
        try:
            os.mkdir("Logs")
            print("Directory /Logs Created ") 
        except FileExistsError:
            print("Directory /Logs already exists")

    def writeLog(self, log):
        now = datetime.now()
        date_time = now.strftime("%m_%d_%Y")

        log = now.strftime("%H:%M:%S") + " | " + log

        with open("Logs/LOG_" + date_time + ".txt", 'a', encoding="utf-8") as logFile:
            logFile.write(log + "\n")
            logFile.close()