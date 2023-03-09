import asyncio

import aiogram.utils.exceptions

import time

from aiogram import Bot

from bot.database.group import Group
from bot.database.user import User
from bot.misc.netschool import get_new_timetables

from bot.misc.env import AdminKeys

admin_id = AdminKeys.ADMID

classrooms = ["5А", "5Б", "5В", "6А", "6Б", "6В", "7А", "7Б", "7В", "8А", "8Б", "9А", "9Б", "10А", "10Б", "11А", "11Б"]


def check_classroom(classroom: str):
    if classroom in classrooms:
        return True
    return False

#TODO УБРАТЬ ДУБЛИРОВАНИЕ КОДА В /bot/misc/util.py и bot/handlers/admin/main.py

async def starting_mailing_message(users_count: int, groups_count: int, date: str, bot: Bot):
    text = "Обнаружены изменения в расписании!"
    text += "\nДата: %s\n" % date.capitalize()
    text += "\nПользователей в базе: %s" % users_count
    text += "\nГрупп в базе: %s" % groups_count
    text += "\n\nОжидаемое время рассылки: %s секунд" % (users_count + groups_count * 0.5)

    await bot.send_message(admin_id, text=text)


async def finished_mailing_message(users_count: int, groups_count: int, messages_count: int, mailing_time, bot: Bot):
    text = "Рассылка окончена!\n"
    text += "\nПользователей обработано: %s" % users_count
    text += "\nГрупп обработано: %s" % groups_count
    text += "\nОтправлено сообщений: %s" % messages_count
    text += "\nЗатрачено времени: %s секунд" % mailing_time
    text += "\nили %s минут, %s секунд" % (mailing_time // 60, mailing_time % 60)

    await bot.send_message(admin_id, text=text)


def format_text(timetable, classroom):
    text = "Новые изменения в расписании!"
    text += "\nДата: %s" % timetable["date"].capitalize()
    text += "\n\nРасписание для %s:" % classroom
    try:
        for lesson in timetable[classroom]:
            text += "\n%s. %s %s" % (lesson['number'], lesson['lesson'], lesson['cabinet'])
    except KeyError as error:
        print(error)
        text += "\nРасписание для %s не найдено" % classroom
    return text.replace("None", "")


def get_time_text(timetable, classroom):
    text = "Расписание звонков:"
    try:
        for lesson in timetable[classroom]:
            text += "\n%s. %s" % (lesson["number"], lesson["time"])
    except KeyError as error:
        print(error)
        text += "\nРасписание для %s не найдено" % classroom
    return text.replace("None", "")


async def check_timetables(sleep_for, bot: Bot):
    while True:
        print("Checking for timetables...")
        timetables = await get_new_timetables(classrooms)
        if len(timetables) > 0:
            print("New timetables found!")
            users = await User.get_all_users()
            groups = await Group.get_all_groups()
            for timetable in timetables:
                await starting_mailing_message(len(users), len(groups), timetable["date"], bot)
                start_time = time.time()
                users_count = 0
                groups_count = 0
                messages_count = 0
                for user in users:
                    user_classrooms = user.get_classrooms()
                    if user_classrooms is None:
                        continue
                    for classroom in user_classrooms:
                        text = format_text(timetable, classroom[0])
                        try:
                            await bot.send_message(user.chat_id, text)
                            messages_count += 1
                            await asyncio.sleep(0.5)
                        except aiogram.utils.exceptions.BotBlocked as error:
                            await user.delete_user()
                            continue
                    users_count += 1
                    # await asyncio.sleep(2)
                for group in groups:
                    if group.classroom is None:
                        continue
                    text = format_text(timetable, group.classroom)
                    try:
                        await bot.send_message(group.chat_id, text)
                        messages_count += 1
                    except aiogram.utils.exceptions.BotKicked as error:
                        await Group.delete_group(group.chat_id)
                        continue
                    groups_count += 1
                    await asyncio.sleep(0.5)
                used_time = int(time.time() - start_time)
                await finished_mailing_message(users_count, groups_count, messages_count, used_time, bot)
            print("Timetables sent succesfully!")
        await asyncio.sleep(sleep_for)
