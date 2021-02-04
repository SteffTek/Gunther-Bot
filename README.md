# Gunther Bot
## Discord Chatbot with AI

Please visit [This Repo](https://github.com/SteffTek/Gunther-Voice) for Gunther Voice - A voice chat Client for Gunther

___

## Prerequisites
| Programm        | Version           |
| --------------- |:-----------------:|
| Python          | 3.7.9       |
| PIP             | 21          |

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

#Other Settings
mongo_db_database = ""
discord_token = ""
discord_command_prefix = "!cb"
```
___
## Startup
Open a console and type:
```
python bot.py
```