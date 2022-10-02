import uuid

from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery

from bot.database.attachment import Attachment
from bot.database.group import Group
from bot.database.user import User
from bot.keyboards.inline import get_main_menu, get_subscribed_classrooms, get_classroom_menu
from bot.misc.util import check_classroom, format_text, classrooms, get_time_text
from bot.misc.xlsx import getTimetable

main_menu_message = "Главное меню."
class_choose_message = "Выберите класс"


async def start(message: Message):
    user = User(chat_id=message.from_user.id, first_name=message.from_user.first_name,
                username=message.from_user.username)
    if User.is_user_new(message.from_user.id):
        user.classroom_key = str(uuid.uuid4())
        print(user.classroom_key)
        await user.write_to_db()
    await message.reply(
        "Привет-привет.\nЭтот бот гениальная альтернатива скачиванию расписания из сетевого!!\nПожалуйста, учитывайте что ошибки всё-таки имеют место быть и иногда расписание может быть неверным! Спасибо :)\n\nПолный список команд доступен через /help")
    await message.answer(
        "/help - вызов этого сообщения\n/subscribe 11Б - подписка на обновления расписания класса\n/latest 11Б - получить новейшее расписание класса\n/menu - глав. меню.")
    await message.answer(main_menu_message, reply_markup=get_main_menu())


async def get_latest(message: Message):
    args = message.get_args().split()
    if len(args) < 1:
        await message.answer("Пожалуйста, укажи класс.\n\nПример: /latest 11Б")
    elif check_classroom(args[0].upper()):
        classroom = args[0].upper()
        timetable = getTimetable("files/" + Attachment.get_latest_attachment(), classrooms)
        text = format_text(timetable, classroom)
        await message.answer(text)
    else:
        await message.answer("Пожалуйста, укажи класс.\n\nПример: /latest 11Б")


async def send_help(message: Message):
    await message.answer(
        "/help - вызов этого сообщения\n/subscribe 11Б - подписка на обновления расписания класса\n/latest 11Б - получить новейшее расписание класса\n/menu - главное меню")


async def subscribe_timetables(message: Message):
    args = message.get_args().split()
    if len(args) < 1:
        await message.answer(
            "Ну и на какой класс тебя подписывать?"
            "\nДля подписки на расписания, напиши \"/subscribe 11Б\""
            "\nЯ надеюсь ты понял, что вместо 11Б надо твой класс написать")

    else:
        if message.chat.type == 'private':
            classroom = args[0].upper()
            user = User.get_user_by_id(message.from_user.id)
            if check_classroom(classroom):
                await user.add_classroom(classroom)
                await message.answer("Ты успешно подписан на расписания %s!!" % classroom)
            else:
                await message.answer("В старшей школе такого класса нет!!")

        else:
            if Group.is_group_new(message.chat.id):
                group = Group(message.chat.id)
                await group.write_to_db()
            classroom = args[0].upper()
            if check_classroom(classroom):
                group = Group(message.chat.id, classroom)
                await group.add_classroom()
                await message.answer("Группа успешно подписана на обновления %s" % classroom)
            else:
                await message.answer("В старшей школе такого класса нет.")


async def unsubscribe_timetables(message: Message):
    args = message.get_args().split()
    if message.chat.type == 'private':
        user = User.get_user_by_id(message.from_user.id)
        await user.remove_classroom() if len(args) < 1 else await user.remove_classroom(args[0].upper())
        await message.answer("Понял принял, отписал.")
    else:
        group = Group(chat_id=message.chat.id)
        await group.remove_classroom()
        await message.answer("Группа отписана от обновлений.")


async def send_main_menu(message: Message):
    if message.chat.type == 'private':
        await message.answer(main_menu_message, reply_markup=get_main_menu())


async def sub_menu(call: CallbackQuery):
    await call.message.edit_text(class_choose_message, reply_markup=get_classroom_menu("subscribe"))


async def latest_menu(call: CallbackQuery):
    await call.message.edit_text(class_choose_message, reply_markup=get_classroom_menu("latest"))


async def unsub_menu(call: CallbackQuery):
    await call.message.edit_text(class_choose_message,
                                 reply_markup=get_subscribed_classrooms(User.get_user_by_id(call.from_user.id)))


async def time_menu(call: CallbackQuery):
    await call.message.edit_text(class_choose_message, reply_markup=get_classroom_menu("time"))


async def subscribe(call: CallbackQuery):
    user = User.get_user_by_id(call.from_user.id)
    classroom = call.data.split()[1]
    await user.add_classroom(classroom)
    await call.message.answer("Вы успешно подписаны на обновления %s" % classroom)
    await call.message.edit_text(main_menu_message, reply_markup=get_main_menu())


async def latest(call: CallbackQuery):
    classroom = call.data.split()[1]
    timetable = getTimetable("files/" + Attachment.get_latest_attachment(), classrooms)
    text = format_text(timetable, classroom)
    await call.message.answer(text)
    await call.message.edit_text(main_menu_message, reply_markup=get_main_menu())


async def time(call: CallbackQuery):
    classroom = call.data.split()[1]
    timetable = getTimetable("files/" + Attachment.get_latest_attachment(), classrooms)
    text = get_time_text(timetable, classroom)
    await call.message.answer(text)
    await call.message.edit_text(main_menu_message, reply_markup=get_main_menu())


async def unsubscribe(call: CallbackQuery):
    user = User.get_user_by_id(call.from_user.id)
    args = call.data.split()
    if len(args) > 1:
        await user.remove_classroom(args[1])
        await call.message.answer("Вы успешно отписаны от %s" % args[1])
    else:
        await user.remove_classroom()
        await call.message.answer("Вы успешно отписаны от всех классов.")
    await call.message.edit_text(main_menu_message, reply_markup=get_main_menu())


async def back(call: CallbackQuery):
    await call.message.edit_text(main_menu_message, reply_markup=get_main_menu())


def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(get_latest, commands=['latest'])
    dp.register_message_handler(send_help, commands=['help'])
    dp.register_message_handler(subscribe_timetables, commands=['subscribe'])
    dp.register_message_handler(unsubscribe_timetables, commands=['unsubscribe'])
    dp.register_message_handler(send_main_menu, commands=['menu'])
    dp.register_callback_query_handler(time_menu, lambda callback_query: callback_query.data == "time_menu")
    dp.register_callback_query_handler(sub_menu, lambda callback_query: callback_query.data == "sub_menu")
    dp.register_callback_query_handler(latest_menu, lambda callback_query: callback_query.data == "latest_menu")
    dp.register_callback_query_handler(unsub_menu, lambda callback_query: callback_query.data == "unsub_menu")
    dp.register_callback_query_handler(time, lambda callback_query: "time" in callback_query.data)
    dp.register_callback_query_handler(unsubscribe, lambda callback_query: "unsubscribe" in callback_query.data)
    dp.register_callback_query_handler(subscribe, lambda callback_query: "subscribe" in callback_query.data)
    dp.register_callback_query_handler(latest, lambda callback_query: "latest" in callback_query.data)
    dp.register_callback_query_handler(back, lambda callback_query: callback_query.data == "main_menu")
