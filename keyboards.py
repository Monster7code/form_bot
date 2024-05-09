from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder

start_keyboard = ReplyKeyboardBuilder()
start_keyboard.add(types.KeyboardButton(text="👾 Поехали"))

default_keyboard = ReplyKeyboardBuilder()
default_keyboard.add(types.KeyboardButton(text="Назад"))


def edit_keyboard_choice_friend(ban_list=[]):
    choice_friend_keyboard = InlineKeyboardBuilder()
    dict_categories_choice_friend = {
        "Друзей и знакомых": types.InlineKeyboardButton(text="Друзей и знакомых", callback_data="friend"),
        "Собутыльников": types.InlineKeyboardButton(text="Собутыльников", callback_data="drunk"),
        "Отношения на ночь": types.InlineKeyboardButton(text="Отношения на ночь", callback_data="love_night"),
        "Любовные отношения": types.InlineKeyboardButton(text="Любовные отношения", callback_data="love"),
        "Единомышлиников": types.InlineKeyboardButton(text="Единомышлиников", callback_data="social"),
        "Назад": types.InlineKeyboardButton(text="Назад", callback_data="back"),
        "Отправить": types.InlineKeyboardButton(text="Отправить", callback_data="submit")}
    for ban_word in ban_list:
        if dict_categories_choice_friend.get(ban_word) is not None:
            dict_categories_choice_friend.pop(ban_word)

    row = 0
    row_list = []
    for button in dict_categories_choice_friend.values():
        if row % 2 == 0:
            choice_friend_keyboard.row(*row_list)
            row_list.clear()
        row += 1
        row_list.append(button)
    else:
        choice_friend_keyboard.row(*row_list)
    return choice_friend_keyboard


def soul_keyboard(ban_list=[]):
    choice_soul_keyboard = InlineKeyboardBuilder()
    dict_categories_choice_soul = {
        "Прогулки": types.InlineKeyboardButton(text="Прогулки", callback_data="walk"),
        "Прогулки с друзьями": types.InlineKeyboardButton(text="Прогулки с друзьями", callback_data="walk_friend"),
        "Прогулки с алкоголем": types.InlineKeyboardButton(text="Прогулки с алкоголем", callback_data="walk_drunk"),
        "Бар": types.InlineKeyboardButton(text="Бар", callback_data="bar"),
        "Клуб": types.InlineKeyboardButton(text="Клуб", callback_data="club"),
        "Кальянная": types.InlineKeyboardButton(text="Кальянная", callback_data="hookah"),
        "Походы": types.InlineKeyboardButton(text="Походы", callback_data="journey"),
        "Спорт": types.InlineKeyboardButton(text="Спорт", callback_data="sport"),
        "Настольные игры": types.InlineKeyboardButton(text="Настольные игры", callback_data="table_game"),
        "Назад": types.InlineKeyboardButton(text="Назад", callback_data="back_soul"),
        "Отправить": types.InlineKeyboardButton(text="Отправить", callback_data="submit_soul"),

    }
    for ban_word in ban_list:
        if dict_categories_choice_soul.get(ban_word) is not None:
            dict_categories_choice_soul.pop(ban_word)

    row = 0
    row_list = []
    for button in dict_categories_choice_soul.values():
        if row % 2 == 0:
            choice_soul_keyboard.row(*row_list)
            row_list.clear()
        row += 1
        row_list.append(button)
    else:
        choice_soul_keyboard.row(*row_list)
    return choice_soul_keyboard


drunk_keyboard = ReplyKeyboardBuilder()
drunk_keyboard.row(types.KeyboardButton(text="Очень часто"),
                   types.KeyboardButton(text="Часто"),
                   types.KeyboardButton(text="Иногда"))
drunk_keyboard.row(types.KeyboardButton(text="Очень редко"),
                   types.KeyboardButton(text="Не пью совсем"),
                   types.KeyboardButton(text="Назад"))


sochial_network_keyboard = ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True, keyboard=[[types.KeyboardButton(text="Vk"),
                                                                                  types.KeyboardButton(text="Telegram"),
                                                                                  types.KeyboardButton(text="И VK и Telegram"),
                                                                                  types.KeyboardButton(text="Назад")]])


new_people_keyboard = ReplyKeyboardBuilder()
new_people_keyboard.row(types.KeyboardButton(text="Крайне негативно"),
                            types.KeyboardButton(text="Негативно"),
                            types.KeyboardButton(text="Нейтрально"))
new_people_keyboard.row(types.KeyboardButton(text="Отлично! люблю знакомства"),
                        types.KeyboardButton(text="Назад"))

final_keyboard = ReplyKeyboardBuilder()
final_keyboard.add(types.KeyboardButton(text="Отправить"), types.KeyboardButton(text="Назад"))