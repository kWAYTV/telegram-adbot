import os
from src.modules.utils.logger import Logger
from src.modules.helper.config import Config

defaultConfig = """
# Telegram Advertiser - discord.gg/kws

# Telegram API Settings
api_id: # Your Telegram API ID
api_hash: "" # Your Telegram API Hash
phone_number: "" # Your Telegram phone number with country code

# Tool Settings
groups_file: "src/data/input/groups.txt" # File containing groups to message
message_file: "src/data/input/message.txt" # File containing the message to send
autoreply_file: "src/data/input/autoreply.txt" # File containing the autoreply message to send
autoreply_switch: True # Whether or not to send an autoreply message
between_messages_delay: 17 # Delay to wait between messages in seconds
after_groups_messaged_delay: 1800 # Delay to wait after all groups have been messaged in seconds
premium_user: False # Whether or not you are a premium user

# Discord Webhook Settings
nickname: "" # Telegram account nickname where you want to be pinged
webhook_switch: True # Whether or not to send discord webhooks
webhook_url: "" # Discord webhook URL
"""

class FileManager():

    def __init__(self):
        self.logger = Logger()
        self.config = Config()

    # Function to check if the input files are valid
    def check_input(self):

        # if there is no config file, create one.
        if not os.path.isfile("config.yaml"):
            self.logger.log("INFO", "Config file not found, creating one...")
            open("config.yaml", "w+").write(defaultConfig)
            self.logger.log("INFO", "Successfully created config.yml, please fill it out and try again.")
            exit()

        # if the folder /src/data/sessions/ doesn't exist, create it.
        if not os.path.isdir("src/data/sessions/"):
            self.logger.log("INFO", "Sessions folder not found, creating one...")
            os.mkdir("src/data/sessions/")

        # if there's no autoreply message in /src/data/input/autoreply.txt and it's turned on, exit the tool.
        if self.config.autoreply_switch and os.stat(self.config.autoreply_file).st_size == 0:
            self.logger.log("ERROR", "There is no autoreply message in /src/data/input/autoreply.txt, please add one and try again.")
            exit()

        # if there is no emails in /src/data/input/emails.txt, exit the tool.
        if os.stat(self.config.groups_file).st_size == 0:
            self.logger.log("ERROR", "There is no emails in /src/data/input/emails.txt, please add some emails and try again.")
            exit()

        # if there is no emails in /src/data/input/proxies.txt, exit the tool.
        if os.stat(self.config.message_file).st_size == 0:
            self.logger.log("ERROR", "There is no emails in /src/data/input/proxies.txt, please add some proxies and try again.")
            exit()