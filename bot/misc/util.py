import asyncio

import aiogram.utils.exceptions
from aiogram import Bot

from bot.database.group import Group
from bot.database.user import User
from bot.misc.netschool import get_new_timetables

classrooms = ["5А", "5Б", "5В", "6А", "6Б", "6В", "7А", "7Б", "7В", "8А", "8Б", "9А", "9Б", "10А", "10Б", "11А", "11Б"]


def check_classroom(classroom: str):
    if classroom in classrooms:
        return True
    return False


def format_text(timetable, classroom):
    text = "Новые изменения в расписании!"
    text += "\nДата: %s"%timetable["date"].capitalize()
    text += "\n\nРасписание для %s:" % classroom
    try:
        for lesson in timetable[classroom]:
            text += "\n%s. %s %s" % (lesson['number'], lesson['lesson'], lesson['cabinet'])
    except KeyError as error:
        print(error)
        text += "\nРасписание для %s не найдено"%classroom
    return text.replace("None", "")


def get_time_text(timetable, classroom):
    text = "Расписание звонков:"
    try:
        for lesson in timetable[classroom]:
            text += "\n%s. %s"%(lesson["number"], lesson["time"])
    except KeyError as error:
        print(error)
        text += "\nРасписание для %s не найдено"%classroom
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
                for user in users:
                    user_classrooms = user.get_classrooms()
                    if user_classrooms is None:
                        continue
                    for classroom in user_classrooms:
                        text = format_text(timetable, classroom[0])
                        try:
                            await bot.send_message(user.chat_id, text)
                            await asyncio.sleep(1)
                        except aiogram.utils.exceptions.BotBlocked as error:
                            print(error)
                            await user.delete_user()
                            continue
                    await asyncio.sleep(2)
                for group in groups:
                    if group.classroom is None:
                        continue
                    text = format_text(timetable, group.classroom)
                    try:
                        await bot.send_message(group.chat_id, text)
                    except aiogram.utils.exceptions.BotKicked as error:
                        print(error)
                        await Group.delete_group(group.chat_id)
                        continue
                    await asyncio.sleep(1)
            print("Timetables sent succesfully!")
        await asyncio.sleep(sleep_for)
