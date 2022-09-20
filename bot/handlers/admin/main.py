import asyncio

import aiogram.utils.exceptions
from aiogram import Dispatcher, Bot
from aiogram.dispatcher.filters import IDFilter
from aiogram.types import Message

from bot.database.group import Group
from bot.database.user import User

from bot.misc.env import AdminKeys

admin_id = AdminKeys.ADMID


async def send_all(message: Message):
    users = await User.get_all_users()
    for user in users:
        text = message.text.replace("/all ", "")
        try:
            await message.bot.send_message(user.chat_id, text)
        except aiogram.utils.exceptions.BotBlocked as error:
            print(error)
            await user.delete_user()
            continue
        await asyncio.sleep(1)


async def send_all_groups(message: Message):
    groups = await Group.get_all_groups()
    for group in groups:
        text = message.text.replace("/gall", "")
        try:
            await message.bot.send_message(group.chat_id, text)
        except aiogram.utils.exceptions.BotKicked as error:
            print(error)
            await group.delete_group()
            continue
        await asyncio.sleep(1)

async def get_count_of_users(message: Message):
        count = User.get_count_of_users()
        await message.reply(str(count))

def register_admin_handlers(dp: Dispatcher):
    dp.register_message_handler(send_all, IDFilter(user_id=admin_id), commands=['all'])
    dp.register_message_handler(send_all_groups, IDFilter(user_id=admin_id), commands=['gall'])
    dp.register_message_handler(get_count_of_users, IDFilter(user_id=admin_id), commands=['howmuch'])
