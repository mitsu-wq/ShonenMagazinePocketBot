from os import getenv, environ
from time import sleep
from loguru import logger
from dotenv import load_dotenv, find_dotenv
from CustomOrigamiBot import CustomOrigamiBot
from botscommands import BotsCommands

# 14079602755231591802

def main():
    """Initialize and start the Telegram manga bot.

    Loads environment variables, validates required variables, initializes the bot,
    registers commands, and starts the bot in an infinite loop.
    """
    environ.pop("TOKEN")
    environ.pop("email_address")
    environ.pop("password")
    load_dotenv(dotenv_path=find_dotenv(),
                verbose=True,
                override=True)

    token = getenv("TOKEN")

    if token is None:
        logger.error(f"Missing environment variable: TOKEN")
        exit(1)

    data = {
        "email_address": getenv("EMAIL_ADDRESS"),
        "password": getenv("PASSWORD")
    }

    bot = CustomOrigamiBot(token)

    bot.add_commands(BotsCommands(bot, data))

    bot.start()
    logger.info(f"{bot.name} is started")
    while True:
        sleep(1.5)

if __name__ == '__main__':
    main()