import asyncio
import json

from config import BOT_TOKEN, CHANNEL_ID
from telegram_bot import TelegramBot


async def main():

    bot = TelegramBot(BOT_TOKEN, CHANNEL_ID)

    with open("questions.json", "r", encoding="utf-8") as f:
        questions = json.load(f)

    if len(questions) == 0:
        print("No questions found.")
        return

    await bot.send_quiz(questions[0])


if __name__ == "__main__":
    asyncio.run(main())
