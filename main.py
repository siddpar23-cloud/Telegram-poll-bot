import asyncio
import json

from config import BOT_TOKEN, CHANNEL_ID, QUESTIONS_PER_DAY
from telegram_bot import TelegramBot

async def main():
    bot = TelegramBot(BOT_TOKEN, CHANNEL_ID)

    with open("questions.json", "r", encoding="utf-8") as f:
        questions = json.load(f)

    if not questions:
        print("No questions found.")
        return

    limit = min(QUESTIONS_PER_DAY, len(questions))

    for i in range(limit):
        await bot.send_quiz(questions[i])

        if i != limit - 1:
            await asyncio.sleep(45)

if __name__ == "__main__":
    asyncio.run(main())