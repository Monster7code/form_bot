from aiogram.fsm.state import StatesGroup, State


class From(StatesGroup):
    start_form = State()
    age_form = State()
    city_form = State()
    about_form = State()
    choice_friend_form = State()
    drunk_form = State()
    choice_soul_form = State()
    sochial_network_form = State()
    conflict_rate_from = State()
    new_people_from = State()
    link_form = State()
    final_form = State()
    change_city = State()


