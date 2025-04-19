import asyncio
import io
import os
import zipfile
import aiohttp
from aiohttp import ClientError
from json import JSONDecodeError
from loguru import logger
from utils import is_number
from math import ceil

from CustomOrigamiBot import CustomOrigamiBot
from origamibot.types import InputMediaPhoto
from getchapter import GetChapter
from exception import GetChapterFailed

class BotsCommands:
    """Command handler for Telegram bot to fetch manga chapters.

    Args:
        bot (CustomOrigamiBot): The Telegram bot instance.
        data (dict): Authentication data with email_address and password.
    """

    def __init__(self, bot: CustomOrigamiBot, data: dict) -> None:
        self.bot = bot
        self.data = data

    async def _send_media(self, chat_id, input_medias: list):
        """Send media as a group or single photo.

        Args:
            chat_id: The Telegram chat ID.
            input_medias (list): List of InputMediaPhoto objects.

        Returns:
            None
        """
        for i in range(0, len(input_medias), 10):
            if len(input_medias) - i == 1:
                self.bot.send_photo(chat_id, input_medias[-1].media, input_medias[-1].caption)
            else:
                await self.bot.send_media_group(chat_id, media=input_medias[i:i+10])

    async def _get_chapter_async(self, chat_id, value: str, username: str, as_zip: bool = False):
        """Asynchronous helper to fetch and send a manga chapter.

        Args:
            chat_id: The Telegram chat ID.
            value (str): The chapter ID.
            username (str): The username of the requesting user.
            as_zip (bool): If True, send as ZIP file; otherwise, send as media group.

        Returns:
            None

        Raises:
            GetChapterFailed: If chapter retrieval fails.
            ClientError: If a network error occurs.
            JSONDecodeError: If JSON parsing fails.
        """
        logger.info(f"Trying get chapter {value} for {username}..")

        msg = await GetChapter(value, self.data["email_address"], self.data["password"])
        title, chapter, pages = msg

        self.bot.send_message(chat_id, f"{title} - {chapter}")

        if as_zip:
            self.bot.send_message(chat_id, "Creating ZIP archive, please wait...")
            zip_buffer = io.BytesIO()
            async with aiohttp.ClientSession() as session:
                with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                    for i, url in enumerate(pages):
                        async with session.get(url) as response:
                            if response.status != 200:
                                continue
                            image_data = await response.read()
                            zip_file.writestr(f"page_{i+1}.jpg", image_data)
            zip_buffer.seek(0)
            await self.bot.send_document(chat_id, zip_buffer, filename=f"{title}_{chapter}")
        else:
            input_medias = [InputMediaPhoto(media=item, caption=str(i+1), parse_mode='html') 
                            for i, item in enumerate(pages)]
            await self._send_media(chat_id, input_medias)
            logger.info(f"Successfully sent chapter {value} with {len(input_medias)} pages")

    def get_chapter(self, message, value: str):
        """Fetch and send a manga chapter to the user.

        Validates the chapter ID, retrieves chapter data, and sends pages as a media group or single photo.
        Chapter ID must be a 20-digit number.

        Args:
            message: The Telegram message object containing user information and chat ID.
            value (str): The chapter ID (expected to be a 20-digit number).

        Returns:
            None
        """
        if not is_number(value) or len(value) != 20:
            logger.error(f"Invalid chapter id: {value}")
            self.bot.send_message(message.chat.id, "Invalid chapter id. It must be a 20-digit number.")
            return

        try:
            asyncio.run(self._get_chapter_async(
                message.chat.id, value, message.from_user.username
            ))
        except GetChapterFailed as e:
            logger.error(f"Failed to get chapter: {e}")
            self.bot.send_message(message.chat.id, str(e))
        except ClientError as e:
            logger.error(f"Network error while fetching chapter: {e}")
            self.bot.send_message(message.chat.id, "Network error. Please try again later.")
        except JSONDecodeError as e:
            logger.error(f"Invalid JSON data: {e}")
            self.bot.send_message(message.chat.id, "Failed to parse chapter data.")
        except Exception as e:
            logger.error(f"Failed to get chapter: {e}")
            self.bot.send_message(message.chat.id, "An error occurred. Please try again.")
    
    def get_chapter_zip(self, message, value: str):
        """Fetch and send a manga chapter to the user as a ZIP archive.

        Validates the chapter ID, retrieves chapter data, and sends pages as a ZIP file.
        Chapter ID must be a 20-digit number.

        Args:
            message: The Telegram message object containing user information and chat ID.
            value (str): The chapter ID (expected to be a 20-digit number).

        Returns:
            None
        """
        if not is_number(value) or len(value) != 20:
            logger.error(f"Invalid chapter id: {value}")
            self.bot.send_message(message.chat.id, "Invalid chapter id. It must be a 20-digit number.")
            return

        try:
            asyncio.run(self._get_chapter_async(
                message.chat.id, value, message.from_user.username, as_zip=True
            ))
        except GetChapterFailed as e:
            logger.error(f"Failed to get chapter: {e}")
            self.bot.send_message(message.chat.id, str(e))
        except ClientError as e:
            logger.error(f"Network error while fetching chapter: {e}")
            self.bot.send_message(message.chat.id, "Network error. Please try again later.")
        except JSONDecodeError as e:
            logger.error(f"Invalid JSON data: {e}")
            self.bot.send_message(message.chat.id, "Failed to parse chapter data.")
        except Exception as e:
            logger.error(f"Failed to get chapter: {e}", exc_info=True)
            self.bot.send_message(message.chat.id, "An error occurred. Please try again.")