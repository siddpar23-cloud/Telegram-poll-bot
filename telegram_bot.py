from telegram import Bot
from telegram.constants import ParseMode
import json

class TelegramBot:

    def __init__(self, token, channel):
        self.bot = Bot(token)
        self.channel = channel

    async def send_quiz(self, question):

        await self.bot.send_poll(
            chat_id=self.channel,
            question=question["question"],
            options=question["options"],
            type="quiz",
            correct_option_id=question["correct"],
            is_anonymous=True
        )

        if question.get("solution"):
            await self.bot.send_message(
                chat_id=self.channel,
                text="📖 Explanation\n\n"+question["solution"],
                parse_mode=ParseMode.HTML
            )
