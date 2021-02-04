import asyncio
import websockets
import ast
import json
import speech_recognition as sr
import wave
import os
import threading

from tools import settings

class WSS:
    def __init__(self, dc_bot):
        self.dc_bot = dc_bot
        self.r = sr.Recognizer()
        #self.websocketserver()
        x = threading.Thread(target=self.websocketserver())

    def websocketserver(self):
        loop = asyncio.get_event_loop()

        async def run(websocket, path):
            async for jsn in websocket:

                message = json.loads(jsn)

                if "binary" in message:
                    loop.create_task(speechToText(websocket, message))
                else:
                    print("WS > " + message["content"])
                    formatted = await formatMessage(message["content"])

                    if formatted is None:
                        return
                    if isinstance(formatted,dict):
                        print("WS ! Banned Words > ", str(formatted))
                        return

                    loop.create_task(sendResponse(websocket, formatted, message))

        async def formatMessage(string):
            # Bad Word Check
            bannedWords = self.dc_bot.main.badWords.containsBad(string)
            if len(bannedWords) > 0:
                return {"err": "banned.word", "words": bannedWords}

            return string

        async def speechToText(websocket, message):

            data = bytearray(message["binary"]["data"])

            audio_path = os.path.join("user_audio", message["author"]["userID"] + ".wav")
            os.makedirs(audio_path)

            with wave.open(audio_path, "wb") as out_f:
                out_f.setnchannels(2)
                out_f.setsampwidth(2) # number of bytes
                out_f.setframerate(44100)
                out_f.writeframesraw(data)

            harvard = sr.AudioFile(audio_path)
            with harvard as source:
                audio = self.r.record(source)

            recognized = self.r.recognize_google(audio, language='de-DE')
            message["recognized"] = recognized
            del message["binary"]

            os.remove(audio_path)

            dump = json.dumps(message)

            await websocket.send(dump)

        async def sendResponse(websocket, data, original):
            statement = self.dc_bot.bot.get_response(data)
            msg = statement.text
            print("WS < ", msg, "; Confidence: ", statement.confidence)

            original["content"] = msg
            original["confidence"] = statement.confidence
            dump = json.dumps(original)

            await websocket.send(dump)

        def start():
            print("Starting Websocket Server...")
            start_server = websockets.serve(run, "", settings.wss_port, max_size=12800000, read_limit=65536, write_limit=65536)
            loop.run_until_complete(start_server)
            print("Websocket Server started!")


        start()
