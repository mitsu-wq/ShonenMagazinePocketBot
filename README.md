# Shonen Magazine Pocket Bot
A Telegram bot for fetching manga chapters from pocket.shonenmagazine.com.

## Prerequisites

- Python 3.12 or higher
- A Telegram bot token (obtain from BotFather)
- (Optional) Account credentials for pocket.shonenmagazine.com (email and password)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/mitsu-wq/ShonenMagazinePocketBot/
   cd ShonenMagazinePocketBot
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root with the following variables:

   ```env
   TOKEN=your_telegram_bot_token
   EMAIL_ADDRESS=your_email
   PASSWORD=your_password
   ```

4. Run the bot:

   ```bash
   python main.py
   ```

## Usage

- `/get_chapter <chapter_id>`: Fetches the specified chapter and sends pages as images. The `chapter_id` must be a number.
- `/get_chapter_zip <chapter_id>`: Fetches the specified chapter and sends pages as a ZIP archive. The `chapter_id` must be a number.

## Project Structure

- `main.py`: Entry point for the bot, initializes and starts the bot.
- `botscommands.py`: Handles bot commands (e.g., `/get_chapter`, `/get_chapter_zip`).
- `CustomOrigamiBot.py`: Custom bot class with improved media group sending.
- `getchapter.py`: Fetches manga chapter data from pocket.shonenmagazine.com.
- `utils.py`: Utility functions for text sanitization and dictionary navigation.
- `exception.py`: Custom exception for chapter retrieval failures.

## Troubleshooting

- **Event loop errors**: If you encounter asyncio-related errors (e.g., "object Message can't be used in 'await' expression"), ensure methods like `send_message` are called without `await`, as they are synchronous in OrigamiBot.