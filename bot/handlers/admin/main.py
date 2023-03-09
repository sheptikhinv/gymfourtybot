import asyncio
import time

import aiogram.utils.exceptions
from aiogram import Dispatcher, Bot
from aiogram.dispatcher.filters import IDFilter
from aiogram.types import Message

from bot.database.group import Group
from bot.database.user import User
from bot.misc.env import AdminKeys

admin_id = AdminKeys.ADMID


async def starting_mailing_message(users_count: int, groups_count: int, message_text: str, bot: Bot):
    text = "Инциирована рассылка!"
    text += "\nПользователей в базе: %s" % users_count
    text += "\nГрупп в базе: %s" % groups_count

    text += "\n\nОжидаемое время рассылки: %s секунд" % (users_count + groups_count * 0.5)
    text += "\n\nТекст рассылаемого сообщения:\n\n%s" % message_text

    await bot.send_message(admin_id, text=text)


async def finished_mailing_message(users_count: int, groups_count: int, messages_count: int, mailing_time, bot: Bot):
    text = "Рассылка окончена!\n"
    text += "\nПользователей обработано: %s" % users_count
    text += "\nГрупп обработано: %s" % groups_count
    text += "\nОтправлено сообщений: %s" % messages_count
    text += "\nЗатрачено времени: %s секунд" % mailing_time
    text += "\nили %s минут, %s секунд" % (mailing_time // 60, mailing_time % 60)

    await bot.send_message(admin_id, text=text)


async def send_all(message: Message):
    text = message.text.replace("/all ", "")
    users = await User.get_all_users()
    groups = await Group.get_all_groups()
    start_time = time.time()
    messages_count = 0
    users_count = 0
    groups_count = 0
    await starting_mailing_message(len(users), len(groups), text, message.bot)

    for user in users:
        try:
            await message.bot.send_message(user.chat_id, text)
            messages_count += 1
        except aiogram.utils.exceptions.BotBlocked as error:
            await user.delete_user()
            continue
        users_count += 1
        await asyncio.sleep(0.5)
    for group in groups:
        try:
            await message.bot.send_message(group.chat_id, text)
            messages_count += 1
        except aiogram.utils.exceptions.BotKicked as error:
            await group.delete_group()
            continue
        groups_count += 1
        await asyncio.sleep(0.5)
    used_time = int(time.time() - start_time)
    await finished_mailing_message(users_count, groups_count, messages_count, used_time, message.bot)


async def get_count_of_users(message: Message):
    count = User.get_count_of_users()
    await message.reply(str(count))


def register_admin_handlers(dp: Dispatcher):
    dp.register_message_handler(send_all, IDFilter(chat_id=admin_id, user_id=admin_id), commands=['all'])
    dp.register_message_handler(get_count_of_users, IDFilter(user_id=admin_id), commands=['howmuch'])
