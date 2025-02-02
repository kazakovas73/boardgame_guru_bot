from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from app.constants import WELCOME_MESSAGE, ButtonConstants
from app.utils import UserState

# 🔘 Главное меню клавиатуры
start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=ButtonConstants.SEARCH_BY_NAME_MESSAGE)],
        [KeyboardButton(text=ButtonConstants.SEARCH_BY_PHOTO_MESSAGE)],
        [KeyboardButton(text=ButtonConstants.ADD_NEW_GAME_MESSAGE)],
    ],
    resize_keyboard=True
)

async def _start(message: Message, state: FSMContext):
    await state.set_state(UserState.MAIN_MENU)
    await message.answer(
        WELCOME_MESSAGE,
        reply_markup=start_kb
    )