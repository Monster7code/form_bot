from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from conec import *

start_keyboard = ReplyKeyboardBuilder()
start_keyboard.add(types.KeyboardButton(text="👾 Поехали"))

default_keyboard = ReplyKeyboardBuilder()
default_keyboard.add(types.KeyboardButton(text="Назад"))



def edit_keyboard_choice_friend(ban_list=[]):
    dict_categories_choice_friend = {
        "Друзей и знакомых": types.InlineKeyboardButton(text="Друзей и знакомых", callback_data="friend"),
        "Собутыльников": types.InlineKeyboardButton(text="Собутыльников", callback_data="drunk"),
        "Отношения на ночь": types.InlineKeyboardButton(text="Отношения на ночь", callback_data="love_night"),
        "Любовные отношения": types.InlineKeyboardButton(text="Любовные отношения", callback_data="love"),
        "Единомышлиников": types.InlineKeyboardButton(text="Единомышлиников", callback_data="social"),
        "Назад": types.InlineKeyboardButton(text="Назад", callback_data="back"),
        "Отправить": types.InlineKeyboardButton(text="Отправить", callback_data="submit")}
    choice_friend_keyboard = InlineKeyboardBuilder()
    for key in dict_categories_choice_friend.keys():
        if ban_list.count(key) > 1:
            ban_list.pop(ban_list.index(key))
            ban_list.pop(ban_list.index(key))

    for ban_word in ban_list:
        if dict_categories_choice_friend.get(ban_word) is not None:
            button = dict_categories_choice_friend.get(ban_word)

            dict_categories_choice_friend.get(ban_word).text = "✅" + button.text

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
    for key in dict_categories_choice_soul.keys():
        if ban_list.count(key) > 1:
            ban_list.pop(ban_list.index(key))
            ban_list.pop(ban_list.index(key))
    for ban_word in ban_list:
        if dict_categories_choice_soul.get(ban_word) is not None:
            button = dict_categories_choice_soul.get(ban_word)

            dict_categories_choice_soul.get(ban_word).text = "✅" + button.text

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


drunk_keyboard = InlineKeyboardBuilder()
drunk_keyboard.row(types.InlineKeyboardButton(text="Очень часто", callback_data="always_drunk"),
                   types.InlineKeyboardButton(text="Часто", callback_data="often_drunk"),
                   types.InlineKeyboardButton(text="Иногда", callback_data="sometimes_drunk"))
drunk_keyboard.row(types.InlineKeyboardButton(text="Очень редко", callback_data="rarely_drunk"),
                   types.InlineKeyboardButton(text="Не пью совсем", callback_data="not_drunk"),
                   types.InlineKeyboardButton(text="Назад", callback_data="back_drunk"))

sochial_network_keyboard = InlineKeyboardBuilder()
sochial_network_keyboard.row(types.InlineKeyboardButton(text="Vk", callback_data="vk"),
                             types.InlineKeyboardButton(text="Telegram", callback_data="tg"))
sochial_network_keyboard.row(types.InlineKeyboardButton(text="И VK и Telegram", callback_data="vk_and_tg"),
                             types.InlineKeyboardButton(text="Назад", callback_data="back_sochial"))


new_people_keyboard = InlineKeyboardBuilder()
new_people_keyboard.row(types.InlineKeyboardButton(text="Крайне негативно", callback_data="new_very_negative"),
                            types.InlineKeyboardButton(text="Негативно", callback_data="new_negative"),
                            types.InlineKeyboardButton(text="Нейтрально", callback_data="new_neutral"))
new_people_keyboard.row(types.InlineKeyboardButton(text="Отлично! люблю знакомства", callback_data="new_cool"),
                        types.InlineKeyboardButton(text="Назад", callback_data="new_back"))

final_keyboard = ReplyKeyboardBuilder()
final_keyboard.add(types.KeyboardButton(text="Отправить"), types.KeyboardButton(text="Назад"))


def create_invite_keyboard(user_id):
    invite_keyboard = InlineKeyboardBuilder()
    invite_keyboard.row(types.InlineKeyboardButton(text="✅ Принять", callback_data=f"accept|{user_id}"),
                                types.InlineKeyboardButton(text="❌ Отклонить", callback_data=f"decline|{user_id}"))
    return invite_keyboard


def create_add_or_drop_on_group_keyboard(user_id, action):
    add_on_group_keyboard = InlineKeyboardBuilder()
    add_on_group_keyboard.row(types.InlineKeyboardButton(text="✅ Да, мы уверены",
                                                         callback_data=f"{action}|{user_id}"),
                                types.InlineKeyboardButton(text="Назад", callback_data=f"back_actions|{user_id}"))
    return add_on_group_keyboard


def create_city_keyboard(user_id):
    cites = get_cities()

    city_keyboard = InlineKeyboardBuilder()
    for city in cites:
        city_keyboard.row(types.InlineKeyboardButton(text=f"{city[0]}", callback_data=f"city|{user_id}|{city[0]}"))

    return city_keyboard


def create_change_city_keyboard():
    cites = get_cities()

    city_keyboard = InlineKeyboardBuilder()
    for city in cites:
        city_keyboard.row(types.InlineKeyboardButton(text=f"{city[0]}", callback_data=f"change_city|{city[0]}"))

    city_keyboard.row(types.InlineKeyboardButton(text=f"Назад", callback_data=f"change_city_back"))
    return city_keyboard