# ![alt text](https://raw.githubusercontent.com/SteffTek/Gunther-Bot/main/avatar.png "Gunther Image") Gunther Bot
## Discord Chatbot with AI

Please visit [this Repo](https://github.com/SteffTek/Gunther-Voice) for Gunther Voice - A voice chat bot for Gunther.

Gunther Bot uses *advanced Algorithms™* to deliver a unique Discord Chat experience. This bot is __at this stage__ only meant to be deployed to a single Discord Guild.

You need to train the bot with your own Data or usage of [Chatterbot Corpus Data](https://chatterbot.readthedocs.io/en/stable/corpus.html) to train it yourself. An example of training with corpus data can be found at the ```bot.py```.

## Click for [Releases](https://github.com/SteffTek/Gunther-Bot/releases)
___
## Prerequisites
| Programm        | Version           |
| --------------- |:-----------------:|
| Python          | 3.7.9       |
| PIP             | 21          |
| MongoDB         | Any Version |

| Python Module        | Version           |
| --------------- |:-----------------:|
| Chatterbot Py   | Latest      |
| Websockets Py   | Latest      |
| SpeechRecognition Py | Latest |
| Discord Py | Latest |

___
## Setup
Rename the ```default.settings.py``` file inside the tools folder to ```settings.py``` and alter the settings.

```python
#Auto Ban Settings
spam_limit = 10
spam_time = 10

#Needed for Gunther Voice
wss_port = 8765
enable_wss = False

#Should the bot Learn from Conversations
enable_learning = True

#Moderation Settings
mod_role = ""
chatchannel = 0
logchannel = 0

#Whitelisted Channels where Gunther will randomly Chat and Listen
whitelisted_channels = [
    "",
]

#Whitlisted Websites Gunther will learn (e.g. Gifs)
whitelisted_websites = [
    "tenor.com"
]

#MongoDB Settings
"""Auth String for Mongo DB Server"""
mongo_db_database = "mongodb://USER:PASSWD@SERVER:PORT/DB"

#Discord Instance Settings
discord_token = ""
discord_command_prefix = "!cb"
```
___
## Startup
Open a console and type:
```
python bot.py
```