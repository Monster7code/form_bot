import asyncio

import aiogram
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from aiogram import F
from keyboards import *
from states import *
import re
from conec import *


id_group = ""
id_admin = ""

class Vote:
    col_for_add = 0
    col_for_drop = 0
    list_of_voters = []
    id_mes_del = aiogram.types.message.Message
    id_mes_add = aiogram.types.message.Message

    def __init__(self):
        self.col_for_add = 0
        self.col_for_drop = 0
        self.list_of_voters = []

    def append_col_for_add(self):
        self.col_for_add += 1

    def append_col_for_drop(self):
        self.col_for_drop += 1

    def append_list_votes(self, user_id):

        if user_id in self.list_of_voters:
            return False
        self.list_of_voters.append(user_id)
        return True


# token suki 6323493760:AAH9r9cDHBTnMecU18g3bVY8mKsTGqgvkPk
bot = Bot("7030266156:AAEU91OszQav7VJDOsGbKqSs7cUs-1G09B0")
loop = asyncio.get_event_loop()
dp = Dispatcher(Bot=bot, loop=loop, storage=MemoryStorage(), parse_mode='HTML')


async def start():
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        return dp


@dp.message(Command("start"))
async def any_message(message: Message, state: FSMContext):
    #create_db_and_table()

    await message.answer(f"Добро пожаловать!",
                         reply_markup=ReplyKeyboardRemove())
    await message.answer("👾Привет! Ищешь компанию?\nЯ помогу тебе в неё попасть,"
                         " осталось только заполнить анкету на вступление, поехали?",
                         reply_markup=start_keyboard.as_markup(resize_keyboard=True))


@dp.message(F.text.lower() == "👾 поехали")
async def form(message: Message, state: FSMContext):
    await state.set_state(From.start_form)
    await message.answer("Как вас зовут?",
                         reply_markup=default_keyboard.as_markup(resize_keyboard=True))


@dp.message(From.start_form)
async def start_from(message: Message, state: FSMContext):
    if message.text == "Назад":
        await state.clear()
        await message.answer("Вы вернулись на главную",
                             reply_markup=start_keyboard.as_markup(resize_keyboard=True))
    else:
        await state.update_data(name=message.text)
        await state.set_state(From.age_form)
        await message.answer(f"Приятно познакомиться, {message.text}!\nСколько вам лет?",
                             reply_markup=default_keyboard.as_markup(resize_keyboard=True))


@dp.message(From.age_form)
async def age_from(message: Message, state: FSMContext):
    if message.text == "Назад":
        await state.set_state(From.start_form)
        await message.answer("Как вас зовут?",
                             reply_markup=default_keyboard.as_markup(resize_keyboard=True))
    else:

        pattern = r'^(\d{1,7})$'
        age = re.search(pattern, message.text)
        if age:
            await state.update_data(age=message.text)
            await state.set_state(From.city_form)
            await message.answer(f"Отлично!\nИз какого вы города?",
                                 reply_markup=default_keyboard.as_markup(resize_keyboard=True))
        else:
            await message.answer("Укажите корректный возраст!",

                                 reply_markup=default_keyboard.as_markup(resize_keyboard=True))


@dp.message(From.city_form)
async def city_from(message: Message, state: FSMContext):
    if message.text == "Назад":
        await state.set_state(From.age_form)
        await message.answer("Укажите свой возраст!",
                             reply_markup=default_keyboard.as_markup(resize_keyboard=True))
    else:
        await state.update_data(city=message.text)
        await state.set_state(From.about_form)
        await message.answer(f"Расскажите о себе",
                             reply_markup=default_keyboard.as_markup(resize_keyboard=True))


@dp.message(From.about_form)
async def about_from(message: Message, state: FSMContext):
    if message.text == "Назад":
        await state.set_state(From.city_form)
        await message.answer("Из какого вы города?",
                             reply_markup=default_keyboard.as_markup(resize_keyboard=True))
    else:
        await state.update_data(about=message.text)
        await state.update_data(banlist=[])
        await state.set_state(From.choice_friend_form)
        await message.answer(f"Кого бы вы хотели себе найти?",
                             reply_markup=edit_keyboard_choice_friend().as_markup(resize_keyboard=True))


@dp.callback_query(F.data.in_(['drunk', 'friend', 'social', 'love_night', 'love', 'back', 'submit']))
async def process_buttons_press(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    banlist = data.get("banlist")
    if callback.data == 'back':
        await callback.message.delete()
        await state.set_state(From.about_form)
        await bot.send_message(callback.from_user.id, f"Расскажите о себе",
                               reply_markup=default_keyboard.as_markup(resize_keyboard=True))
    elif callback.data == 'submit':
        if len(banlist) == 0:
            await bot.send_message(callback.from_user.id, f"Пожалуйста, сначала выбирете что-нибудь из списка?")
        else:
            await state.update_data(banlist_result=banlist)
            await callback.message.delete()
            await state.set_state(From.drunk_form)
            await bot.send_message(callback.from_user.id, f"Как часто вы выпиваете?",
                                   reply_markup=drunk_keyboard.as_markup(resize_keyboard=True))
    else:
        if callback.data == 'drunk':
            banlist.append("Собутыльников")
        elif callback.data == 'friend':
            banlist.append("Друзей и знакомых")
        elif callback.data == 'social':
            banlist.append("Единомышлиников")
        elif callback.data == 'love_night':
            banlist.append("Отношения на ночь")
        elif callback.data == 'love':
            banlist.append("Любовные отношения")

        await state.update_data(banlist=banlist)

        await callback.answer()
        await callback.message.edit_text(
            text='выбрано',
            reply_markup=edit_keyboard_choice_friend(banlist).as_markup(resize_keyboard=True)
        )


@dp.callback_query(F.data.in_(['always_drunk', 'often_drunk', 'sometimes_drunk', 'rarely_drunk', 'not_drunk',
                               'back_drunk']))
async def about_drunk(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'back_drunk':
        await callback.message.delete()
        await state.set_state(From.choice_friend_form)
        await bot.send_message(callback.from_user.id, f"Кого бы вы хотели себе найти?",
                               reply_markup=ReplyKeyboardRemove())
        await bot.send_message(callback.from_user.id, f"Выберите из списка:",
                               reply_markup=edit_keyboard_choice_friend().as_markup(resize_keyboard=True))
    else:
        for row in callback.message.reply_markup.inline_keyboard:
            for button in row:
                if button.callback_data == callback.data:
                    await state.update_data(drunk=button.text)
                    break
        await state.set_state(From.choice_soul_form)
        await state.update_data(banlist_soul=[])
        await bot.send_message(callback.from_user.id, f"Отлично",
                               reply_markup=ReplyKeyboardRemove())
        await bot.send_message(callback.from_user.id, f"Выберите то что вам по душе:",
                               reply_markup=soul_keyboard().as_markup(resize_keyboard=True))
        await callback.message.delete()
        await callback.answer()


@dp.callback_query(F.data.in_(['walk', 'walk_drunk', 'walk_friend', 'bar',
                               'club', 'hookah', 'back_soul', 'submit_soul', 'journey', 'sport', 'table_game']))
async def process_buttons_press(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    banlist = data.get("banlist_soul")
    if callback.data == 'back_soul':
        await callback.message.delete()
        await state.set_state(From.drunk_form)
        await bot.send_message(callback.from_user.id, f"Как часто вы выпиваете?",
                               reply_markup=ReplyKeyboardRemove())
        await bot.send_message(callback.from_user.id, f"Выберите из списка:",
                               reply_markup=drunk_keyboard.as_markup(resize_keyboard=True))
    elif callback.data == 'submit_soul':
        if len(banlist) == 0:
            await bot.send_message(callback.from_user.id, f"Пожалуйста, сначала выбирете что-нибудь из списка?")
        else:
            await state.update_data(banlist_soul_result=banlist)
            await callback.message.delete()
            await state.set_state(From.sochial_network_form)
            await bot.send_message(callback.from_user.id, f"Чем пользуетесь на постоянной основе?",
                                   reply_markup=sochial_network_keyboard.as_markup(resize_keyboard=True))
    else:
        if callback.data == 'walk':
            banlist.append("Прогулки")
        elif callback.data == 'walk_drunk':
            banlist.append("Прогулки с алкоголем")
        elif callback.data == 'walk_friend':
            banlist.append("Прогулки с друзьями")
        elif callback.data == 'bar':
            banlist.append("Бар")
        elif callback.data == 'club':
            banlist.append("Клуб")
        elif callback.data == 'hookah':
            banlist.append("Кальянная")
        elif callback.data == 'journey':
            banlist.append("Походы")
        elif callback.data == 'sport':
            banlist.append("Спорт")
        elif callback.data == 'table_game':
            banlist.append("Настольные игры")

        await state.update_data(banlist=banlist)

        await callback.answer()
        await callback.message.edit_text(
            text=f'{banlist[len(banlist) - 1]} выбрано',
            reply_markup=soul_keyboard(banlist).as_markup(resize_keyboard=True)
        )


@dp.callback_query(F.data.in_(['vk', 'tg', 'vk_and_tg', 'back_sochial']))
async def sochial_network_form(callback: CallbackQuery, state: FSMContext):
    if callback.data == "back_sochial":
        await state.set_state(From.choice_soul_form)
        await state.update_data(banlist_soul=[])
        await bot.send_message(chat_id=callback.from_user.id, text=f"Выберите то что вам по душе:",
                               reply_markup=soul_keyboard().as_markup(resize_keyboard=True))
        await callback.message.delete()
    else:
        for row in callback.message.reply_markup.inline_keyboard:
            for button in row:
                if button.callback_data == callback.data:
                    await state.update_data(sochial_network=button.text)
                    break

        await callback.message.delete()
        await state.set_state(From.conflict_rate_from)
        await bot.send_message(chat_id=callback.from_user.id, text=f"Оцените свою конфликтность от 1 до 10",
                               reply_markup=default_keyboard.as_markup(resize_keyboard=True))


@dp.message(From.conflict_rate_from)
async def conflict_rate_from(message: Message, state: FSMContext):
    if message.text == "Назад":
        await state.set_state(From.sochial_network_form)
        await message.answer(f"Чем пользуетесь на постоянной основе?",
                             reply_markup=sochial_network_keyboard.as_markup(resize_keyboard=True))
    else:
        pattern = r'^(\d{1,10})$'
        rate = re.search(pattern, message.text)
        if rate:
            if (int(message.text) <= 10) and (int(message.text) >= 0):
                await state.update_data(rate_conflict=message.text)
                await state.set_state(From.new_people_from)
                await message.answer(f"Как вы относитесь к тому чтоб в вашу компанию приходили новенькие люди?",
                                     reply_markup=new_people_keyboard.as_markup(resize_keyboard=True))
            else:
                await message.answer(f"Проверте правильность введенных данных",
                                     reply_markup=default_keyboard.as_markup(resize_keyboard=True))
        else:
            await message.answer(f"Проверте правильность введенных данных",
                                 reply_markup=default_keyboard.as_markup(resize_keyboard=True))


@dp.callback_query(F.data.in_(['new_very_negative', 'new_negative', 'new_neutral', 'new_cool', 'new_back']))
async def about_from(callback: CallbackQuery, state: FSMContext):
    if callback.data == "new_back":
        await state.set_state(From.conflict_rate_from)
        await bot.send_message(text=f"Оцените свою конфликтность от 1 до 10", chat_id=callback.from_user.id,
                               reply_markup=default_keyboard.as_markup(resize_keyboard=True))
        await callback.message.delete()
    else:
        for row in callback.message.reply_markup.inline_keyboard:
            for button in row:
                if button.callback_data == callback.data:
                    await state.update_data(new_people=button.text)
                    break
        await callback.message.delete()
        await state.set_state(From.link_form)
        await bot.send_message(text=f"Пришлите свою страницу в VK (необязательно)\nВведите любой текст для продолжения",
                               chat_id=callback.from_user.id,
                               reply_markup=default_keyboard.as_markup(resize_keyboard=True))


@dp.message(From.link_form)
async def about_from(message: Message, state: FSMContext):
    if message.text == "Назад":
        await state.set_state(From.new_people_from)
        await message.answer(f"Как вы относитесь к тому чтоб в вашу компанию приходили новенькие люди?",
                             reply_markup=new_people_keyboard.as_markup(resize_keyboard=True))
    else:
        await state.update_data(login=message.text)
        await state.set_state(From.final_form)
        await message.answer(f"Отправить форму?",
                             reply_markup=final_keyboard.as_markup(resize_keyboard=True))


@dp.message(From.final_form)
async def about_from(message: Message, state: FSMContext):
    if message.text == "Назад":
        await state.set_state(From.link_form)
        await message.answer(f"Пришлите свою страницу в VK (необязательно)\nВведите любой текст для продолжения",
                             reply_markup=default_keyboard.as_markup(resize_keyboard=True))
    elif message.text == "Отправить":
        data = await state.get_data()
        name = data.get("name")
        age = data.get("age")
        city = data.get("city")
        about = data.get("about")
        banlist_result = data.get("banlist_result")
        drunk = data.get("drunk")
        banlist_soul_result = data.get("banlist_soul_result")
        sochial_network = data.get("sochial_network")
        rate_conflict = data.get("rate_conflict")
        new_people = data.get("new_people")
        login = data.get("login")

        text = (f"💭<b>От пользователя:</b> {message.from_user.full_name}\n\n\n"
                f"•<b>Имя:</b> {name}\n"
                f"<b>•Возраст:</b> {age}\n"
                f"<b>•Город:</b> {city}\n"
                f"<b>•Информация:</b> {about}\n"
                f"<b>•Предпочтения в друзьях:</b> {''.join(', '.join(banlist_result))}\n"
                f"<b>•Отношение к алкоголю:</b> {drunk}\n"
                f"<b>•Предпочтения в развлечениях:</b> {''.join(', '.join(banlist_soul_result))}\n"
                f"<b>•Социальные сети:</b> {sochial_network}\n"
                f"<b>•Конфликтность:</b> {rate_conflict}\n"
                f"<b>•Отношение к новичкам:</b> {new_people}\n"
                f"<b>•Страница в VK:</b> {login}\n")
        if message.from_user.username is None:
            text += f'<b>•Профиль в телеграме:</b> <a href="{message.from_user.url}">Ссылка на профиль</a>'
        else:
            text += (f'<b>•Профиль в телеграме:</b>'
                     f' <a href="https://t.me/{message.from_user.username}">Ссылка на профиль</a>')
        # id group -1002165833102
        await bot.send_message("-1002165833102", text=text, parse_mode="html",
                               reply_markup=create_invite_keyboard(message.from_user.id).as_markup(),
                               disable_web_page_preview=True)
        await state.set_state(From.final_form)
        await state.clear()
        await message.answer(f"Вы успешно отправили форму",
                             reply_markup=ReplyKeyboardRemove())


@dp.callback_query(lambda call: (call.data[:6] == "accept") or (call.data[:7] == "decline"))
async def accept_decline_user(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    callback_id_user_form_new_rec = data.get("callback_id_user_form")
    if callback_id_user_form_new_rec is None:
        callback_id_user_form_new_rec = {f"callback_{call.data.split("|")[1]}": Vote()}


    else:
        try:
            print(type(callback_id_user_form_new_rec[f"callback_{call.data.split("|")[1]}"]) == Vote)
        except:
            callback_id_user_form_new_rec[f"callback_{call.data.split("|")[1]}"] = Vote()
    await state.update_data(callback_id_user_form=callback_id_user_form_new_rec)
    data = await state.get_data()
    callback_id_user_form_new_rec = data.get("callback_id_user_form")
    if call.data[:7] == "decline":
        if callback_id_user_form_new_rec.get(f"callback_{call.data.split("|")[1]}").append_list_votes(
                call.from_user.id):

            callback_id_user_form_new_rec.get(f"callback_{call.data.split("|")[1]}").append_col_for_drop()
            if callback_id_user_form_new_rec.get(f"callback_{call.data.split("|")[1]}").col_for_drop < 3:
                try:
                    await bot.delete_message(chat_id="-1002165833102",
                                             message_id=
                                             callback_id_user_form_new_rec.get(f"callback_{call.data.split("|")[1]}").id_mes_del.message_id)
                except:
                    pass
                text = (f"Чтобы отклонить участника нужно, чтобы проголосовали ещё"
                        f" {3 - callback_id_user_form_new_rec.get(f"callback_{call.data.split("|")[1]}").col_for_drop}")
            else:
                try:
                    await bot.delete_message(chat_id="-1002165833102",
                                             message_id=
                                             callback_id_user_form_new_rec.get(f"callback_{call.data.split("|")[1]}").id_mes_del.message_id)
                    await bot.delete_message(chat_id="-1002165833102",
                                             message_id=
                                             callback_id_user_form_new_rec.get(
                                                 f"callback_{call.data.split("|")[1]}").id_mes_add.message_id)
                except:
                    pass
                del callback_id_user_form_new_rec[(f"callback_{call.data.split("|")[1]}")]
                text = "Вы уверены, что хотите отклонить участника"
                await (call.message.edit_reply_markup
                       (inline_message_id=str(call.message.message_id),
                        reply_markup=
                        create_add_or_drop_on_group_keyboard(call.from_user.id, "drop").as_markup()))
            try:
                callback_id_user_form_new_rec.get(f"callback_{call.data.split("|")[1]}").id_mes_del = await bot.send_message(chat_id=call.message.chat.id, text=text)
            except:
                pass
            await state.update_data(callback_id_user_form=callback_id_user_form_new_rec)
        else:
            await bot.send_message(chat_id="-1002165833102", text=f"{call.from_user.first_name} ты уже голосовал")
        await call.answer()
    elif call.data[:6] == "accept":
        if callback_id_user_form_new_rec.get(f"callback_{call.data.split("|")[1]}").append_list_votes(
                call.from_user.id):

            callback_id_user_form_new_rec.get(f"callback_{call.data.split("|")[1]}").append_col_for_add()
            if callback_id_user_form_new_rec.get(f"callback_{call.data.split("|")[1]}").col_for_add < 3:
                try:
                    await bot.delete_message(chat_id="-1002165833102",
                                             message_id=
                                             callback_id_user_form_new_rec.get(f"callback_{call.data.split("|")[1]}").id_mes_add.message_id)
                except:
                    pass
                text = (f"Чтобы добавить участника нужно, чтобы проголосовали ещё"
                        f" {3 - callback_id_user_form_new_rec.get(f"callback_{call.data.split("|")[1]}").col_for_add}")
            else:
                try:

                    await bot.delete_message(chat_id="-1002165833102",
                                             message_id=
                                             callback_id_user_form_new_rec.get(f"callback_{call.data.split("|")[1]}").id_mes_add.message_id)
                    await bot.delete_message(chat_id="-1002165833102",
                                             message_id=
                                             callback_id_user_form_new_rec.get(
                                                 f"callback_{call.data.split("|")[1]}").id_mes_del.message_id)
                except:
                    pass
                del callback_id_user_form_new_rec[(f"callback_{call.data.split("|")[1]}")]
                text = "Вы уверены, что хотите добавить участника"
                await (call.message.edit_reply_markup
                       (inline_message_id=str(call.message.message_id),
                        reply_markup=
                        create_add_or_drop_on_group_keyboard(call.from_user.id, "add").as_markup()))

            try:
                callback_id_user_form_new_rec.get(f"callback_{call.data.split("|")[1]}").id_mes_add = await bot.send_message(chat_id=call.message.chat.id, text=text)
            except:
                pass

            await state.update_data(callback_id_user_form=callback_id_user_form_new_rec)

        else:
            await bot.send_message(chat_id="-1002165833102", text=f"{call.from_user.first_name} ты уже голосовал")
        await call.answer()


@dp.callback_query(lambda call: (call.data[:3] == "add") or (call.data[:4] == "drop")
                                or (call.data[:12] == "back_actions"))
async def add_on_group_or_not(call: types.CallbackQuery, state: FSMContext):
    if call.data[:12] == "back_actions":
        await call.message.edit_reply_markup(inline_message_id=str(call.message.message_id),
                                             reply_markup=create_invite_keyboard(call.data.split("|")[1]).as_markup())
        await bot.send_message(chat_id=call.message.chat.id, text="Хорошо, подумайте ещё")
    elif call.data[:3] == "add":

        await call.message.edit_reply_markup(inline_message_id=str(call.message.message_id), reply_markup=None)
        await call.answer()
        await bot.send_message(chat_id=call.message.chat.id, text="Выберите ссылку на чат:",
                               reply_markup=create_city_keyboard(call.data.split("|")[1]).as_markup())

    elif call.data[:4] == "drop":
        await call.message.edit_reply_markup(inline_message_id=str(call.message.message_id), reply_markup=None)
        await call.answer()
        await bot.send_message(chat_id=call.message.chat.id, text="Вы отклонили участника")


@dp.callback_query(lambda call: (call.data[:4] == "city"))
async def choice_city(call: types.CallbackQuery, state: FSMContext):
    city = call.data.split("|")[2]
    user_id = call.data.split("|")[1]
    link = get_link(city)
    await bot.send_message(chat_id=call.message.chat.id, text="Пользователю отправленны данные для входа")
    text = (f'<b>Ваша анкета одобрена</b>✅\n<b><i>Ссылка на вступление:</i></b>\n{link}\n'
            '<b>Чат для общения</b> с '
            'участниками находится в закреплённом сообщении канала <b>"Актуальные ресурсы"</b>')
    await bot.send_message(chat_id=user_id, text=text, parse_mode="html")
    await call.answer()
    await call.message.delete()


@dp.message(F.text.lower() == "назад")
async def form(message: Message, state: FSMContext):
    await message.answer("Как вас зовут?",
                         reply_markup=default_keyboard.as_markup(resize_keyboard=True))


@dp.message(Command("admin"))
async def any_message(message: Message, state: FSMContext):

    if str(message.from_user.id) == "605578928":
        await message.answer("Добро пожаловать в админ панель!\n"
                             "Для смены ссылки нажмите на город и введите новую ссылку",
                             reply_markup=create_change_city_keyboard().as_markup(resize_keyboard=True))


@dp.callback_query(lambda call: ((call.data[:11] == "change_city") or (call.data == "change_city_back")))
async def change_city(call: types.CallbackQuery, state: FSMContext):
    if call.data == "change_city_back":
        await bot.send_message(chat_id=call.from_user.id, text=f"Добро пожаловать!",
                               reply_markup=ReplyKeyboardRemove())
        await bot.send_message(chat_id=call.from_user.id, text="👾Привет! Ищешь компанию?\nЯ помогу тебе в неё попасть,"
                             " осталось только заполнить анкету на вступление, поехали?",
                             reply_markup=start_keyboard.as_markup(resize_keyboard=True))
    else:
        await state.update_data(changer_city=call.data.split("|")[1])
        await state.set_state(From.change_city)
        await bot.send_message(chat_id=call.from_user.id, text="Теперь введите новую ссылку",
                               reply_markup=default_keyboard.as_markup())
    await call.message.delete()


@dp.message(From.change_city)
async def change_city(message: Message, state: FSMContext):
    if message.text == "Назад":
        await message.answer("Добро пожаловать в админ панель!\n"
                                  "Для смены ссылки нажмите на город и введите новую ссылку",
                                  reply_markup=create_change_city_keyboard().as_markup(resize_keyboard=True))
    else:
        data = await state.get_data()
        city = data.get("changer_city")
        if update_link_city(city, message.text):
            await message.answer("Ссылка успешно заменена")
            await message.answer("Добро пожаловать в админ панель!\n"
                                 "Для смены ссылки нажмите на город и введите новую ссылку",
                                 reply_markup=create_change_city_keyboard().as_markup(resize_keyboard=True))
        else:
            await message.answer("При замене ссылки произошла ошибка!\n"
                                 "Для смены ссылки нажмите на город и введите новую ссылку",
                                 reply_markup=create_change_city_keyboard().as_markup(resize_keyboard=True))
    await state.clear()
if __name__ == "__main__":
    asyncio.run(start())
