import io
from origamibot import OrigamiBot
from typing import IO, Literal, Union, List, Optional, override
from origamibot.core.teletypes import InputMedia, ReplyMarkup, Message
from origamibot.core import api_request

class CustomOrigamiBot(OrigamiBot):
    """Custom Telegram bot with improved media group sending.

    Extends OrigamiBot to handle InputMedia objects with optional file attributes.
    """
    def __init__(self, token):
        """Initialize the bot with a Telegram API token.

        Args:
            token (str): Telegram Bot API token.
        """
        super().__init__(token)

    @override
    async def send_media_group(self,
                         chat_id: Union[int, str],
                         media: List[InputMedia],
                         disable_notification: Optional[bool] = None,
                         reply_to_message_id: Optional[bool] = None,
                         protect_content: Optional[bool] = None
                         ) -> Message:
        """Send a group of photos or videos as an album.

        Supports InputMedia objects with optional file attributes for local file uploads.

        Args:
            chat_id (Union[int, str]): Unique identifier for the target chat or username.
            media (List[InputMedia]): List of media objects (2–10 items).
            disable_notification (Optional[bool]): Sends the message silently if True.
            reply_to_message_id (Optional[bool]): ID of the message to reply to.
            protect_content (Optional[bool]): Protects the content from forwarding and saving.

        Returns:
            Message: The sent message object.

        Raises:
            AssertionError: If the number of media items is not between 2 and 10.
        """
        assert 10 >= len(media) >= 2, 'Invalid number of media, must be 2-10'

        data = {
            'chat_id': chat_id,
            'media': [m.unfold() for m in media],
            'disable_notification': disable_notification,
            'reply_to_message_id': reply_to_message_id,
            'protect_content': protect_content
        }

        files = {}
        for media_item in media:
            if hasattr(media_item, 'file') and media_item.file and isinstance(media_item.file.value, tuple):
                attach_name, file_path = media_item.file.value
                if attach_name and file_path:
                    files[attach_name] = file_path

        return api_request.request(
            self.token,
            'sendMediaGroup',
            data,
            files,
            'message'
        )
    
    @override
    async def send_photo(self,
                         chat_id: Union[int, str],
                         photo: Union[str, io.IOBase],
                         caption: Union[str, None] = None,
                         parse_mode: Optional[Literal["HTML", "MarkdownV2", "Markdown"]] = None,
                         disable_notification: Optional[bool] = None,
                         reply_to_message_id: Optional[int] = None,
                         reply_markup: Optional[ReplyMarkup] = None,
                         protect_content: Optional[bool] = None
                         ) -> Message:
        """Use this method to send photos.

        Args:
            chat_id (Union[int, str]): Unique identifier for the target chat or username.
            photo (Union[str, io.IOBase]): URL, file path, or file-like object containing the photo.
            caption (Union[str, None]): Photo caption.
            parse_mode (Optional[str]): Parse mode for the caption ("HTML", "MarkdownV2", "Markdown").
            disable_notification (Optional[bool]): Sends the message silently if True.
            reply_to_message_id (Optional[int]): ID of the message to reply to.
            reply_markup (Optional[ReplyMarkup]): Additional interface options.
            protect_content (Optional[bool]): Protects the content from forwarding and saving.

        Returns:
            Message: The sent message object.
        """
        data = {
            'chat_id': chat_id,
            'caption': caption,
            'parse_mode': parse_mode,
            'disable_notification': disable_notification,
            'reply_to_message_id': reply_to_message_id,
            'reply_markup': (reply_markup.unfold() if reply_markup is not None else None),
            'protect_content': protect_content
        }

        if isinstance(photo, io.IOBase):
            photo.seek(0)
            return api_request.request(
                self.token,
                'sendPhoto',
                data,
                files={'photo': ('photo.jpg', photo, 'image/jpeg')},
                excpect='message'
            )
        else:
            data['photo'] = photo
            return api_request.request(
                self.token,
                'sendPhoto',
                data,
                excpect='message'
            )
    
    @override
    async def send_document(self, chat_id: Union[int, str], document: Union[str, io.BytesIO], filename: str, **kwargs) -> Message:
        """Send a document to a chat.

        Args:
            chat_id (Union[int, str]): Unique identifier for the target chat or username.
            document (Union[str, io.BytesIO]): Path to the file or BytesIO object.
            **kwargs: Additional parameters for the Telegram API.

        Returns:
            Message: The sent message object.
        """
        if isinstance(document, io.BytesIO):
            document.seek(0)
            files = {'document': (f'{filename}.zip', document, 'application/zip')}
            data = {'chat_id': chat_id, **kwargs}
            return api_request.request(self.token, 'sendDocument', data, files, 'message')
        return super().send_document(chat_id, document, **kwargs)