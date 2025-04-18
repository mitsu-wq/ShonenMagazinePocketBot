# Shonen Magazine Pocket Bot
A Telegram bot for fetching manga chapters from pocket.shonenmagazine.com.

## Prerequisites

- Python 3.11 or higher
- A Telegram bot token (obtain from BotFather)
- Account credentials for pocket.shonenmagazine.com (email and password)

## Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd <repository-name>
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

- Send the command `/get_chapter <chapter_id>` to the bot, where `<chapter_id>` is a 20-digit number representing the chapter ID on pocket.shonenmagazine.com.

## Project Structure

- `main.py`: Entry point for the bot, initializes and starts the bot.
- `botscommands.py`: Handles bot commands (e.g., `/get_chapter`).
- `CustomOrigamiBot.py`: Custom bot class with improved media group sending.
- `getchapter.py`: Fetches manga chapter data from pocket.shonenmagazine.com.
- `utils.py`: Utility functions for text sanitization and dictionary navigation.
- `exception.py`: Custom exception for chapter retrieval failures.

## Troubleshooting

- **Event loop errors**: If you encounter asyncio-related errors (e.g., "object Message can't be used in 'await' expression"), ensure methods like `send_message` and `send_photo` are called without `await`, as they are synchronous in OrigamiBot.