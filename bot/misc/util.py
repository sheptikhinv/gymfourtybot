import asyncio
import time

import aiogram.utils.exceptions
from aiogram import Bot

from bot.database.group import Group
from bot.database.user import User
from bot.handlers.admin.main import starting_mailing_message, finished_mailing_message, errors_found
from bot.misc.env import AdminKeys
from bot.misc.netschool import get_new_timetables

admin_id = AdminKeys.ADMID

classrooms = ["5А", "5Б", "5В", "5Г", "5Д", "6А", "6Б", "6В", "6Г", "7А", "7Б", "7В", "8А", "8Б", "8В", "9А", "9Б", "10А", "10Б", "11А", "11Б"]


def check_classroom(classroom: str):
    if classroom in classrooms:
        return True
    return False


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
    recent_timetable = {}
    while True:
        print("Checking for timetables...")
        timetables = await get_new_timetables(classrooms)
        if len(timetables) > 0:
            print("New timetables found!")
            users = await User.get_all_users()
            groups = await Group.get_all_groups()
            for timetable in timetables:
                await starting_mailing_message(len(users), len(groups), timetable["date"].capitalize(), bot)
                start_time = time.time()  # Старт таймера рассылки для статы
                users_count = 0
                groups_count = 0
                messages_count = 0
                for user in users:
                    user_classrooms = user.get_classrooms()
                    if user_classrooms is None:
                        continue
                    for classroom in user_classrooms:
                        if recent_timetable != {}:
                            if timetable["date"] == recent_timetable["date"] and timetable[classroom[0]] == \
                                    recent_timetable[classroom[0]]:
                                continue
                        text = format_text(timetable, classroom[0])  ##TODO: ПОФИКСИТЬ ЕБАНОЕ classroom[0]
                        try:
                            await bot.send_message(user.chat_id, text)
                            messages_count += 1
                            await asyncio.sleep(0.5)
                        except (aiogram.utils.exceptions.Unauthorized, aiogram.utils.exceptions.ChatNotFound) as error:
                            await user.delete_user()
                        except aiogram.utils.exceptions.BadRequest as error:
                            await errors_found(users_count, groups_count, error.text, bot)
                        else:
                            users_count += 1
                for group in groups:
                    if group.classroom is None:
                        continue
                    if recent_timetable != {}:
                        if timetable["date"] == recent_timetable["date"] and timetable[group.classroom] == recent_timetable[group.classroom]:
                            continue
                    text = format_text(timetable, group.classroom)
                    try:
                        await bot.send_message(group.chat_id, text)
                        messages_count += 1
                    except (aiogram.utils.exceptions.Unauthorized, aiogram.utils.exceptions.GroupDeactivated,
                            aiogram.utils.exceptions.ChatNotFound) as error:
                        await Group.delete_group(group.chat_id)
                    except aiogram.utils.exceptions.BadRequest as error:
                        await errors_found(users_count, groups_count, error.text, bot)
                    else:
                        groups_count += 1
                    await asyncio.sleep(0.5)
                used_time = int(time.time() - start_time)
                await finished_mailing_message(users_count, groups_count, messages_count, used_time, bot)
            recent_timetable = timetables[-1]
            print("Timetables sent succesfully!")
        await asyncio.sleep(sleep_for)
