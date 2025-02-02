import os
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types.reply_keyboard_remove import ReplyKeyboardRemove
from app.constants import ADD_GAME_REQUEST_MESSAGE, ADD_GAME_SUCCESS_MESSAGE, ADD_NEW_GAME, ASK_QUESTION, FOUND_SIMILAR_GAMES, REQUEST_GAME_NAME_MESSAGE, SELCTED_GAME, escape_markdown
from app.elastic_db import elastic_add_game, elastic_search_game_by_vector
from app.embeddings import get_text_embedding
from app.utils import UserState


async def _search_by_name_handler(message: Message, state: FSMContext):
    await state.set_state(UserState.SEARCH_BY_NAME)
    await message.answer(
        REQUEST_GAME_NAME_MESSAGE,
        reply_markup=ReplyKeyboardRemove(),
    )

async def _search_by_name(message: Message, state: FSMContext, model):
    await state.update_data(name=message.text)
    similar_games = elastic_search_game_by_vector(get_text_embedding(model, message.text))

    await message.answer(escape_markdown(str(await state.get_data())))
    
    if similar_games:
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text=game)]
                for game in similar_games
            ] + [[KeyboardButton(text=escape_markdown(ADD_NEW_GAME + ': ' + message.text))]], resize_keyboard=True
        )

        await state.set_state(UserState.ADD_GAME_CHOICE)
        await message.answer(
            FOUND_SIMILAR_GAMES,
            reply_markup=keyboard
        )
    else:
        await message.answer("No games Please add them in the main menu")