import yaml
from yaml import SafeLoader

class Config():
    def __init__(self):

        with open("config.yaml", "r") as file:
            self.config = yaml.load(file, Loader=SafeLoader)

            # Set the Build version & icon
            self.build_version = "2.3.5"
            self.webhook_icon = "https://i.imgur.com/M1jL4KL.png"

            # Telegram API Settings
            self.api_id = self.config["api_id"]
            self.api_hash = self.config["api_hash"]
            self.phone_number = self.config["phone_number"]

            # Tool Settings
            self.groups_file = self.config["groups_file"]
            self.message_file = self.config["message_file"]
            self.autoreply_file = self.config["autoreply_file"]
            self.autoreply_switch = self.config["autoreply_switch"]
            self.between_messages_delay = self.config["between_messages_delay"]
            self.after_groups_messaged_delay = self.config["after_groups_messaged_delay"]
            self.premium_user = self.config["premium_user"]

            # Discord Webhook Settings
            self.nickname = self.config["nickname"]
            self.webhook_switch = self.config["webhook_switch"]
            self.webhook_url = self.config["webhook_url"]