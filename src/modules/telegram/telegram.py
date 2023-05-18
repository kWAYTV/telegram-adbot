import asyncio, os
from telethon import TelegramClient
from src.modules.utils.logger import Logger
from src.modules.helper.config import Config
from telethon import errors, functions, types
from src.modules.discord.webhooks import Webhooks
from telethon.tl.functions.channels import JoinChannelRequest, LeaveChannelRequest

class Shiller:

    def __init__(self):
        
        # Set the colors for the logs
        self.config = Config()
        self.logger = Logger()
        self.webhook = Webhooks()
        self.client = TelegramClient('src/data/sessions/anon', self.config.api_id, self.config.api_hash, sequential_updates=True)
        self.groups_file_content = open(self.config.groups_file, "r+").read().strip().split("\n")
        self.message_file_content = open(self.config.message_file, "r+", encoding="utf-8").read().strip()

    async def connect_client(self):

        self.logger.log("INFO", "Attempting to login to Telegram...")
        await self.client.connect()

        if not await self.client.is_user_authorized():
            self.logger.log("INFO", "Verification code required, sending it to your Telegram account.")
            await self.client.send_code_request(self.phone_number)
            self.logger.log("INFO", "Sent the verification code to your Telegram account.")

            self.logger.log("INFO", "Input your verification code.")
            code = input("")
            await self.client.sign_in(self.phone_number, code)

        self.user = await self.client.get_me()
        self.logger.log("INFO", "Successfully signed into account {}.".format(self.user.username))

    async def get_groups(self):
        self.logger.log("INFO", "Getting all the groups, this could take a while...")

        group_limit = None
        if self.config.premium_user: group_limit = 400
        else: group_limit = 200

        groups = []
        results = await self.client(functions.messages.GetDialogsRequest(
            offset_date=None,
            offset_id=0,
            offset_peer=types.InputPeerEmpty(),
            limit=group_limit,
            hash=0
        ))
        
        for dialog in results.chats:
            if isinstance(dialog, types.Channel):
                dialog: types.Channel = dialog
                groups.append(dialog)

        self.logger.log("INFO", "Found {} groups.".format(len(groups)))
        return groups

    async def join_groups(self):
        seen = []

        self.logger.log("INPUT", "Do you want to join groups? (y/n)")
        option = input("")
        if option == "" or "n" in option: return
        print("")

        for group in self.groups_file_content:
            if group in seen: continue
            seen.append(group)

            while True:
                try:
                    if "t.me" in group: code = group.split("t.me/")[1]
                    else: code = group

                    await self.client(JoinChannelRequest(code))
                    self.logger.log("SUCCESS", "Joined group {}!".format(group))
                    break
                except errors.FloodWaitError as e:
                    self.logger.log("SLEEP", "Ratelimited for {} seconds.".format(e.seconds))
                    await asyncio.sleep(int(e.seconds))
                except Exception as e:
                    self.logger.log("ERROR", "Failed to join group {}.".format(group))
                    self.webhook.error_webhook("Failed to join group {}.".format(group))
                    break

            await asyncio.sleep(0.8)

    async def leave_groups(self):
        seen = []

        self.logger.log("INPUT", "Do you want to leave groups? (y/n)")
        option = input("")
        if option == "" or "n" in option: return
        print("")

        for group in self.groups_file_content:
            if group in seen: continue
            seen.append(group)

            while True:
                try:
                    if "t.me" in group: code = group.split("t.me/")[1]
                    else: code = group

                    await self.client(LeaveChannelRequest(code))
                    self.logger.log("SUCCESS", "Left group {}!".format(group))
                    break
                except errors.FloodWaitError as e:
                    self.logger.log("SLEEP", "Ratelimited for {} seconds.".format(e.seconds))
                    await asyncio.sleep(int(e.seconds))
                except Exception as e:
                    self.logger.log("ERROR", "Failed to leave group {}.".format(group))
                    self.webhook.error_webhook("Failed to leave group {}.".format(group))
                    break

            await asyncio.sleep(0.8)

    async def send_message(self, group: types.Channel):
        try:
            await self.client.send_message(group, self.message_file_content)
            return True
        except errors.FloodWaitError as e:
            self.logger.log("SLEEP", "Ratelimited for {} seconds.".format(e.seconds))
            self.webhook.error_webhook("Ratelimited for {} seconds.".format(e.seconds))
            await asyncio.sleep(int(e.seconds))
        except Exception as e:
            return e

    async def start_shilling(self):
        sent = 0
        while True:
            try:
                groups = await self.get_groups()
                self.logger.log("INFO", "Starting to advertise! Sent {} messages so far.".format(sent))
                self.webhook.start_shill_webhook(int(len(groups)), int(sent))
                for group in groups:
                    try:
                        last_message = (await self.client.get_messages(group, limit=1))[0]
                        if last_message.from_id.user_id == self.user.id:
                            self.logger.log("INFO", "Skipped group {} as our message is the latest.".format(group.title))
                            continue
                        
                        if await self.send_message(group):
                            self.logger.log("SUCCESS", "Forwarded your message to {}!".format(group.title))
                            sent += 1
                        else:
                            self.logger.log("ERROR", "Failed to forward your message to {}!".format(group.title))

                        # Set title
                        if os.name == 'nt':
                            os.system("title Shillify Telegram • Sent {} messages • discord.gg/kws".format(sent))

                        await asyncio.sleep(int(self.config.between_messages_delay))
                    except Exception as e:
                        self.logger.log("ERROR", "Failed to forward your message to {}! Error: {}".format(group.title, e))
                        self.webhook.error_webhook("Failed to forward your message to {}! Error: {}".format(group.title, e))

            except Exception as e:
                self.logger.log("ERROR", "Failed to get groups. Error: {}".format(e))
                self.webhook.error_webhook("Failed to get groups. Error: {}".format(e))

            self.logger.log("INFO", "Finished shilling, sent {} messages. Waiting {} seconds before shilling again.".format(sent, self.config.after_groups_messaged_delay))
            await self.client.send_message(self.config.nickname, "Finished shilling, sent {} messages. Starting again in {} seconds.".format(sent, self.config.after_groups_messaged_delay))
            self.webhook.finished_webhook(sent)
            await asyncio.sleep(int(self.config.after_groups_messaged_delay))

    async def start(self):
        await self.connect_client()
        await self.client.send_message(self.config.nickname, "Shillify Telegram has started!")
        await self.join_groups()
        await self.leave_groups()
        await self.start_shilling()