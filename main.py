import asyncio
import json
import threading
import os

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

    while True:

        with open("progress.json", "r") as f:
            progress = json.load(f)

        start = progress["last_question"]
        end = min(start + QUESTIONS_PER_DAY, len(questions))

        for i in range(start, end):
            await bot.send_quiz(questions[i])

            with open("progress.json", "w") as f:
                json.dump({"last_question": i + 1}, f)

            await asyncio.sleep(45)

        if end >= len(questions):
            print("All questions completed.")
            break

        await asyncio.sleep(86400)


def start_bot():
    asyncio.run(send_questions())


if __name__ == "__main__":
    thread = threading.Thread(target=start_bot)
    thread.start()

    app.run(host="0.0.0.0", port=10000)
def start_bot():
    print("BOT THREAD STARTED")
    asyncio.run(send_questions())
