import asyncio, os, logging
from src.modules.utils.logger import Logger
from src.modules.helper.config import Config
from src.modules.telegram.telegram import Shiller
from src.modules.discord.webhooks import Webhooks
from src.modules.helper.filemanager import FileManager

# Set title
if os.name == 'nt':
    os.system("title Shillify Telegram • Telegram Autoadvertiser • Starting... • discord.gg/kws")

# Set logging system
logging.basicConfig(handlers=[logging.FileHandler('shillify.log', 'w+', 'utf-8')], level=logging.ERROR, format='%(asctime)s: %(message)s')

class Main():
    def __init__(self) -> None:
        self.logger = Logger()
        self.config = Config()
        self.filemanager = FileManager()
        self.shiller = Shiller()
        self.webhook = Webhooks()

    async def start(self):
        await self.logger.print_logo(self.config.nickname)
        if self.config.webhook_switch: self.webhook.start_tool_webhook()

        # Check input
        self.filemanager.check_input()

        # Start shilling
        await self.shiller.start()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    Tool = Main()
    loop.run_until_complete(Tool.start())