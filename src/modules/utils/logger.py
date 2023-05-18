import os
from datetime import datetime
from colorama import Fore, Style
from src.modules.helper.config import Config
from pystyle import Colors, Colorate, Center

# Clear the console.
clear = lambda: os.system("cls" if os.name in ("nt", "dos") else "clear")

# Logo
logo = """
███████╗██╗  ██╗██╗██╗     ██╗     ██╗███████╗██╗   ██╗
██╔════╝██║  ██║██║██║     ██║     ██║██╔════╝╚██╗ ██╔╝
███████╗███████║██║██║     ██║     ██║█████╗   ╚████╔╝ 
╚════██║██╔══██║██║██║     ██║     ██║██╔══╝    ╚██╔╝  
███████║██║  ██║██║███████╗███████╗██║██║        ██║   
╚══════╝╚═╝  ╚═╝╚═╝╚══════╝╚══════╝╚═╝╚═╝        ╚═╝"""

class Logger:

    def __init__(self):
        
        # Set the colors for the logs
        self.log_types = {
            "INFO": Fore.CYAN,
            "OK": Fore.GREEN,
            "WARNING": Fore.YELLOW,
            "SLEEP": Fore.YELLOW,
            "ERROR": Fore.RED,
            "INPUT": Fore.BLUE,
        }
        self.config = Config()

    # Function to print the logo when the gen starts
    async def print_logo(self, username: str):
        clear()
        print(Center.XCenter(Colorate.Vertical(Colors.white_to_blue, logo, 1)))
        print(Center.XCenter(Colorate.Vertical(Colors.white_to_blue, "────────────────────────────────────────────\n", 1)))
        print(Center.XCenter(Colorate.Vertical(Colors.white_to_blue, f"Welcome, {username}!\n\n", 1)))
        os.system(f"title Shillify Telegram {self.config.build_version} • Telegram Autoadvertiser • I'm ready, {username}! • discord.gg/kws")

    # Function to log messages to the console
    def log(self, type, message):
        color = self.log_types[type]
        now = datetime.now()
        current_time = now.strftime("%d/%m/%Y • %H:%M:%S")
        print(f"{Style.DIM}{current_time} • {Style.RESET_ALL}{Style.BRIGHT}{color}[{Style.RESET_ALL}{type}{Style.BRIGHT}{color}] {Style.RESET_ALL}{Style.BRIGHT}{Fore.WHITE}{message}")