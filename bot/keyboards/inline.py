from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.database.user import User

classrooms = ["5А", "5Б", "5В", "6А", "6Б", "6В", "7А", "7Б", "7В", "8А", "8Б", "9А", "9Б", "10А", "10Б", "11А", "11Б"]


def get_main_menu():
    main_menu = InlineKeyboardMarkup(row_width=2,
                                     inline_keyboard=[
                                         [
                                             InlineKeyboardButton(text='Подписаться', callback_data='sub_menu'),
                                             InlineKeyboardButton(text='Новейшее расп.', callback_data='latest_menu')
                                         ],
                                         [
                                             InlineKeyboardButton(text="Отписаться", callback_data="unsub_menu"),
                                             InlineKeyboardButton(text="Звонки", callback_data='time_menu')
                                         ],
                                         [
                                             InlineKeyboardButton(text='Написать в поддержку 😎',
                                                                  url='https://t.me/gmslava')
                                         ]
                                     ])
    return main_menu


def get_classroom_menu(action):
    subscribe_menu = InlineKeyboardMarkup(row_width=5)
    subscribe_menu.add(InlineKeyboardButton(text="Назад <-", callback_data="main_menu"))
    for classroom in classrooms:
        subscribe_menu.add(InlineKeyboardButton(text=classroom, callback_data="%s %s" %(action, classroom)))
    return subscribe_menu


def get_subscribed_classrooms(user: User):
    menu = InlineKeyboardMarkup(row_width=1)
    menu.add(InlineKeyboardButton(text="Назад <--", callback_data="main_menu"))
    menu.add(InlineKeyboardButton(text="От всех", callback_data="unsubscribe"))
    for classroom in user.get_classrooms():
        menu.add(InlineKeyboardButton(text=classroom[0], callback_data="unsubscribe %s"%classroom))
    return menu
