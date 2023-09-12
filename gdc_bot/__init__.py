import asyncio

from aiogram import Bot, Dispatcher
from aiogram.filters import Command

from gdc_database import db_bot_chats
from gdc_database.db_bot_chats import BotChatData

bot = Bot("6512951342:AAHGL6ynxmKqUZkWbsUg6nJEFTaaoZHbCSg")
dp = Dispatcher()


def send_alert(text: str):
    send_message(f"‼️{text}")


def send_info(text: str):
    send_message(f"📄 {text}")


def send_error(text: str):
    send_message(f"❌ {text}")


async def send_message(text: str):
    global bot
    chats = db_bot_chats.get_bot_chats()

    for chat in chats:
        await bot.send_message(chat.chat_id,
                               f"{text}",
                               parse_mode="HTML")


@dp.message(Command('save_chat'))
async def fd(message):
    global bot
    db_bot_chats.write_bot_chat(BotChatData(id=-1,
                                            chat_id=message.chat.id))
    await bot.send_message(message.chat.id,
                           '👌')


async def start_telegram_log_bot():
    global dp, bot
    await dp.start_polling(bot, skip_updates=True)
