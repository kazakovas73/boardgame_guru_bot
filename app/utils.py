from aiogram.fsm.state import State, StatesGroup

# 🔹 Определяем состояния пользователя
class UserState(StatesGroup):
    MAIN_MENU = State()
    SEARCH_BY_NAME = State()
    SEARCH_BY_PHOTO = State()
    ADD_GAME_NAME = State()
    ADD_GAME_CHOICE = State()
    ADD_GAME_PDF = State()
    SEARCH_RULES = State()