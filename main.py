import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from aiogram import F
from keyboards import *
from states import *
import re


bot = Bot("6323493760:AAH9r9cDHBTnMecU18g3bVY8mKsTGqgvkPk")
loop = asyncio.get_event_loop()
dp = Dispatcher(Bot=bot, loop=loop, storage=MemoryStorage())


async def start():
    try:
        await dp.start_polling(bot)

    finally:
        await bot.session.close()
        return dp


@dp.message(Command("start"))
async def any_message(message: Message, state: FSMContext):
    await state.update_data(user_id=message.from_user.id)
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
    print(banlist)
    if callback.data == 'back':
        await callback.message.delete()
        await state.set_state(From.about_form)
        await bot.send_message(data.get("user_id"), f"Расскажите о себе",
                               reply_markup=default_keyboard.as_markup(resize_keyboard=True))
    elif callback.data == 'submit':
        print(banlist)
        if len(banlist) == 0:
            await bot.send_message(data.get("user_id"), f"Пожалуйста, сначала выбирете что-нибудь из списка?")
        else:
            await state.update_data(banlist_result=banlist)
            await callback.message.delete()
            await state.set_state(From.drunk_form)
            await bot.send_message(data.get("user_id"), f"Как часто вы выпиваете?",
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
            text=f'{banlist[len(banlist)-1]} добавлено',
            reply_markup=edit_keyboard_choice_friend(banlist).as_markup(resize_keyboard=True)
            )


@dp.message(From.drunk_form)
async def about_from(message: Message, state: FSMContext):
    if message.text == "Назад":
        await state.update_data(banlist=[])
        await state.set_state(From.choice_friend_form)
        await message.answer(f"Кого бы вы хотели себе найти?",
                             reply_markup=ReplyKeyboardRemove())
        await message.answer(f"Выберите из списка:",
                             reply_markup=edit_keyboard_choice_friend().as_markup(resize_keyboard=True))
    else:
        await state.update_data(drunk=message.text)
        await state.set_state(From.choice_soul_form)
        await state.update_data(banlist_soul=[])
        await message.answer(f"Отлично",
                             reply_markup=ReplyKeyboardRemove())
        await message.answer(f"Выберите то что вам по душе:",
                             reply_markup=soul_keyboard().as_markup(resize_keyboard=True))


@dp.callback_query(F.data.in_(['walk', 'walk_drunk', 'walk_friend', 'bar',
                               'club', 'hookah', 'back_soul', 'submit_soul', 'journey', 'sport', 'table_game']))
async def process_buttons_press(callback: CallbackQuery, state: FSMContext):

    data = await state.get_data()
    banlist = data.get("banlist_soul")
    if callback.data == 'back_soul':
        await callback.message.delete()
        await state.set_state(From.drunk_form)
        await bot.send_message(data.get("user_id"), f"Как часто вы выпиваете?",
                               reply_markup=ReplyKeyboardRemove())
        await bot.send_message(data.get("user_id"), f"Выберите из списка:",
                               reply_markup=drunk_keyboard.as_markup(resize_keyboard=True))
    elif callback.data == 'submit_soul':
        if len(banlist) == 0:
            await bot.send_message(data.get("user_id"), f"Пожалуйста, сначала выбирете что-нибудь из списка?")
        else:
            await state.update_data(banlist_soul_result=banlist)
            await callback.message.delete()
            await state.set_state(From.sochial_network_form)
            await bot.send_message(data.get("user_id"), f"Чем пользуетесь на постоянной основе?",
                                   reply_markup=sochial_network_keyboard)
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
            text=f'{banlist[len(banlist)-1]} добавлено',
            reply_markup=soul_keyboard(banlist).as_markup(resize_keyboard=True)
            )


@dp.message(From.sochial_network_form)
async def about_from(message: Message, state: FSMContext):
    if message.text == "Назад":
        await state.set_state(From.choice_soul_form)
        await state.update_data(banlist_soul=[])
        await message.answer(f"Выберите то что вам по душе:",
                             reply_markup=soul_keyboard().as_markup(resize_keyboard=True))
    else:
        await state.update_data(sochial_network=message.text)
        await state.set_state(From.conflict_rate_from)
        await message.answer(f"Оцените свою конфликтность от 1 до 10",
                             reply_markup=default_keyboard.as_markup(resize_keyboard=True))


@dp.message(From.conflict_rate_from)
async def about_from(message: Message, state: FSMContext):
    if message.text == "Назад":
        await state.set_state(From.sochial_network_form)
        await message.answer(f"Чем пользуетесь на постоянной основе?",
                             reply_markup=sochial_network_keyboard)
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


@dp.message(From.new_people_from)
async def about_from(message: Message, state: FSMContext):
    if message.text == "Назад":
        await state.set_state(From.conflict_rate_from)
        await message.answer(f"Оцените свою конфликтность от 1 до 10",
                             reply_markup=default_keyboard.as_markup(resize_keyboard=True))
    else:
        await state.update_data(new_people=message.text)
        await state.set_state(From.link_form)
        await message.answer(f"Пришлите свою страницу в VK (необязательно)\nВведите любой текст для продолжения",
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
        await bot.send_message("5805700754", f"От пользователя{message.from_user.full_name}\n"
                                             f"Имя {name}\n"
                               f"Возраст {age}\n"
                               f"Город {city}\n"
                               f"Информация {about}\n"
                               f"Предпочтения в друзьях {banlist_result}\n"
                               f"Отношение к алкоголю {drunk}\n"
                               f"Предпочтения в развлечениях {banlist_soul_result}\n"
                               f"Социальные сети {sochial_network}\n"
                               f"Конфликтность {rate_conflict}\n"
                               f"Отношение к новичкам {new_people}\n"
                               f"Ссылки {login}\n"
                               )
        await state.set_state(From.final_form)
        await message.answer(f"Вы успешно отправили форму",
                             reply_markup=ReplyKeyboardRemove())
if __name__ == "__main__":
    asyncio.run(start())
