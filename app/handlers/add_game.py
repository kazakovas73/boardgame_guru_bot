import os
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types.reply_keyboard_remove import ReplyKeyboardRemove
from app.chunks import extract_text_from_pdf, split_text_with_langchain
from app.constants import ADD_GAME_REQUEST_MESSAGE, ADD_GAME_SUCCESS_MESSAGE, ADD_NEW_GAME, ASK_QUESTION, FOUND_SIMILAR_GAMES, SELCTED_GAME, escape_markdown
from app.elastic_db import create_rules_index, elastic_add_game, elastic_add_rules, elastic_search_game_by_vector
from app.embeddings import get_text_embedding
from app.utils import UserState
import logging

async def _add_game_handler(message: Message, state: FSMContext):
    await state.set_state(UserState.ADD_GAME_NAME)
    await message.answer(
        ADD_GAME_REQUEST_MESSAGE,
        reply_markup=ReplyKeyboardRemove(),
    )

async def _add_game_name(message: Message, state: FSMContext, model):
    emb = get_text_embedding(model, message.text)
    similar_games = elastic_search_game_by_vector(emb)

    await state.update_data(game_name=message.text, emb=emb)

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
        await state.set_state(UserState.ADD_GAME_PDF)
        await message.answer("Please upload the PDF file with the rules")

async def _add_game_choice(message: Message, state: FSMContext):
    if ADD_NEW_GAME + ': ' in message.text:
        await state.set_state(UserState.ADD_GAME_PDF)
        await message.answer(
            "Please upload the PDF file with the rules",
            reply_markup=ReplyKeyboardRemove(),
        )
    else:
        await state.set_state(UserState.SEARCH_RULES)
        await message.answer(escape_markdown(SELCTED_GAME.format(game_name=message.text)), reply_markup=ReplyKeyboardRemove())
        await message.answer(ASK_QUESTION)

async def _add_game_pdf(message: Message, state: FSMContext, bot, model):
    document = message.document
    file_id = document.file_id
    file_name = document.file_name

    UPLOAD_DIR = "uploads/"
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # Загружаем файл
    file_path = f"{UPLOAD_DIR}/{file_name}"
    await bot.download(file_id, destination=file_path)

    await message.answer("Adding game rules to my storage")

    pdf_text = extract_text_from_pdf(file_path)
    chunks = split_text_with_langchain(pdf_text)

    data = await state.get_data()

    await elastic_add_game(data['game_name'], data['emb'])

    await create_rules_index(data['game_name'])

    for chunk in chunks:
        emb = get_text_embedding(model, chunk)
        await elastic_add_rules(data['game_name'], chunk, emb)

    await state.set_state(UserState.SEARCH_RULES)
    await message.answer(ADD_GAME_SUCCESS_MESSAGE)
    await message.answer(ASK_QUESTION)