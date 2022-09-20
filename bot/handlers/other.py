import aiogram.utils.exceptions
from aiogram import Dispatcher
from aiogram.types import Message


async def bot_kicked_handler():
    return True


def register_other_handlers(dp: Dispatcher) -> None:
    dp.register_errors_handler(bot_kicked_handler, exception=aiogram.utils.exceptions.BotKicked)
