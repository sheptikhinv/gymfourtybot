import aiogram.utils.exceptions
from aiogram import Dispatcher
from aiogram.types import Message
from bot.misc.env import AdminKeys


async def bot_kicked_handler():
    return True

async def all_exceptions(exception, update):
    await exception.bot.send_message(AdminKeys.ADMID, str(exception))

def register_other_handlers(dp: Dispatcher) -> None:
    dp.register_errors_handler(bot_kicked_handler, exception=aiogram.utils.exceptions.BotKicked)
    dp.register_errors_handler(all_exceptions)
