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