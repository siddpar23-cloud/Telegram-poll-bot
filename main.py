import asyncio
import json
import threading

from flask import Flask

from config import BOT_TOKEN, CHANNEL_ID, QUESTIONS_PER_DAY
from telegram_bot import TelegramBot

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

async def send_questions():
    bot = TelegramBot(BOT_TOKEN, CHANNEL_ID)

    with open("questions.json", "r", encoding="utf-8") as f:
        questions = json.load(f)

    if not questions:
        print("No questions found.")
        return

    limit = min(QUESTIONS_PER_DAY, len(questions))

    while True:
        for i in range(limit):
            await bot.send_quiz(questions[i])

            if i != limit - 1:
                await asyncio.sleep(45)

        print("Today's questions completed.")
        await asyncio.sleep(86400)


def start_bot():
    asyncio.run(send_questions())


if __name__ == "__main__":
    thread = threading.Thread(target=start_bot)
    thread.start()

    app.run(host="0.0.0.0", port=10000)
