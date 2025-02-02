import sys
import os
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.context import FSMContext

from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram import Router, F
from dotenv import load_dotenv

# Добавляем пути для импортов
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.handlers.search_rules import _search_rules
from handlers.search_game import _search_by_name, _search_by_name_handler
from utils import UserState
from handlers.start import _start
from handlers.add_game import _add_game_choice, _add_game_handler, _add_game_name, _add_game_pdf

from elastic_db import create_text_games_index
from embeddings import EmbeddingModel

# Импортируем обработчики
from constants import ButtonConstants

# Загружаем переменные окружения
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN is missing! Проверь .env файл.")

form_router = Router(name=__name__)

MODEL = EmbeddingModel

# Создаём бота с поддержкой MarkdownV2
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="MarkdownV2"))
dp = Dispatcher()
dp.include_router(form_router)


# Логирование
logging.basicConfig(level=logging.INFO)


@form_router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext) -> None:
    await _start(message, state)

@form_router.message(UserState.MAIN_MENU, F.text == ButtonConstants.ADD_NEW_GAME_MESSAGE)
async def add_game_handler(message: Message, state: FSMContext) -> None:
    await _add_game_handler(message, state)
    
@form_router.message(UserState.ADD_GAME_NAME)
async def add_game_name(message: Message, state: FSMContext) -> None:
    await _add_game_name(message, state, MODEL)

@form_router.message(UserState.ADD_GAME_CHOICE)
async def add_game_choice(message: Message, state: FSMContext) -> None:
    await _add_game_choice(message, state)

@form_router.message(UserState.ADD_GAME_PDF, F.document.mime_type == "application/pdf")
async def add_game_pdf(message: Message, state: FSMContext) -> None:
    await _add_game_pdf(message, state, bot, MODEL)

@form_router.message(UserState.MAIN_MENU, F.text == ButtonConstants.SEARCH_BY_NAME_MESSAGE)
async def search_by_name_handler(message: Message, state: FSMContext) -> None:
    await _search_by_name_handler(message, state)

@form_router.message(UserState.SEARCH_BY_NAME)
async def search_by_name(message: Message, state: FSMContext) -> None:
    await _search_by_name(message, state, MODEL)

@form_router.message(UserState.SEARCH_RULES)
async def search_rules(message: Message, state: FSMContext) -> None:
    await _search_rules(message, state, MODEL)

# 📌 Запуск бота
async def main():
    create_text_games_index()

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())