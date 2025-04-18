from os import getenv
from time import sleep
from loguru import logger
from dotenv import load_dotenv
from origamibot import OrigamiBot
from CustomOrigamiBot import CustomOrigamiBot
from botscommands import BotsCommands

# 14079602755231591802

def main():
    """Initialize and start the Telegram manga bot.

    Loads environment variables, validates required variables, initializes the bot,
    registers commands, and starts the bot in an infinite loop.
    """
    load_dotenv()

    required_env = ["TOKEN", "EMAIL_ADDRESS", "PASSWORD"]
    for var in required_env:
        if not getenv(var):
            logger.error(f"Missing environment variable: {var}")
            exit(1)

    data = {
        "email_address": getenv("EMAIL_ADDRESS"),
        "password": getenv("PASSWORD")
    }

    token = getenv("TOKEN")
    bot = CustomOrigamiBot(token)

    bot.add_commands(BotsCommands(bot, data))

    bot.start()
    logger.info(f"{bot.name} is started")
    while True:
        sleep(1.5)

if __name__ == '__main__':
    main()