from src.modules.helper.config import Config
from discord_webhook import DiscordWebhook, DiscordEmbed

class Webhooks:

    def __init__(self):
        self.config = Config()
        #self.content = f"||<@{self.config.discord_id}>||"
        self.hook = DiscordWebhook(url = self.config.webhook_url, username = "Shillify Telegram", avatar_url = self.config.webhook_icon, rate_limit_retry = True) #, content = self.content)
        self.hookImg = self.config.webhook_icon

    def start_tool_webhook(self):
        if self.config.webhook_switch:
            embed = DiscordEmbed(description = "Starting...", color = 0x036d80)
            embed.set_author(name = "Shillify Telegram", url = "https://kwayservices.top/", icon_url = self.hookImg)
            embed.set_footer(text = f"Shillify Telegram - {self.config.nickname}", icon_url = self.hookImg)
            embed.set_thumbnail(url = self.hookImg)
            embed.set_timestamp()
            self.hook.add_embed(embed)
            self.hook.execute( remove_embeds = True )

    def start_shill_webhook(self, groups, sent_now, sent_total):
        if self.config.webhook_switch:
            embed = DiscordEmbed(description = "Advertising Started!", color = 0xbb95bf)
            embed.set_author(name = "Shillify Telegram", url = "https://kwayservices.top/", icon_url = self.hookImg)
            embed.set_footer(text = f"Shillify Telegram - {self.config.nickname}", icon_url = self.hookImg)
            embed.add_embed_field(name = "Found Groups", value = groups)
            embed.add_embed_field(name = "Sent Now", value = sent_now)
            embed.add_embed_field(name = "Sent Total", value = sent_total)
            embed.set_thumbnail(url = self.hookImg)
            embed.set_timestamp()
            self.hook.add_embed(embed)
            self.hook.execute( remove_embeds = True )

    def error_webhook(self, error):
        if self.config.webhook_switch:
            embed = DiscordEmbed(description = "An error occured!", color = 0xff0000)
            embed.set_author(name = "Shillify Telegram", url = "https://kwayservices.top/", icon_url = self.hookImg)
            embed.add_embed_field(name = "Error", value = error)
            embed.set_footer(text = f"Shillify Telegram - {self.config.nickname}", icon_url = self.hookImg)
            embed.set_thumbnail(url = self.hookImg)
            embed.set_timestamp()
            self.hook.add_embed(embed)
            self.hook.execute( remove_embeds = True )

    def finished_webhook(self, sent_now, sent_total):
        if self.config.webhook_switch:
            embed = DiscordEmbed(color = 0x000000)
            embed.set_author(name = "Shillify Telegram", url = "https://kwayservices.top/", icon_url = self.hookImg)
            embed.add_embed_field(name = "Sent now", value = sent_now)
            embed.add_embed_field(name = "Sent total", value = sent_total)
            embed.set_footer(text = f"Shillify Telegram - {self.config.nickname}", icon_url = self.hookImg)
            embed.set_thumbnail(url = self.hookImg)
            embed.set_timestamp()
            self.hook.add_embed(embed)
            self.hook.execute( remove_embeds = True )