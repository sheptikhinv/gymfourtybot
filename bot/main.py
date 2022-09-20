import asyncio

from aiogram.utils import executor
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from bot.misc import TgKeys
from bot.misc.util import check_timetables
from bot.handlers import register_all_handlers


async def __on_start_up(dp: Dispatcher) -> None:
    register_all_handlers(dp)


def start_bot():
    bot = Bot(token=TgKeys.TOKEN, parse_mode='HTML')
    dp = Dispatcher(bot, storage=MemoryStorage())
    loop = asyncio.get_event_loop()
    loop.create_task(check_timetables(600, bot))
    executor.start_polling(dp, skip_updates=False, on_startup=__on_start_up)
