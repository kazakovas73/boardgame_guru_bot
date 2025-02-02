import re

class CommandsConstants:
    START_COMMAND = "/start"
    HELP_COMMAND = "/help"
    SEARCH_COMMAND = "/search"
    ADD_COMMAND = "/add"

class ButtonConstants:
    SEARCH_BY_PHOTO_MESSAGE = "📷 Search by Photo"
    SEARCH_BY_NAME_MESSAGE = "🔤 Search by Name"
    ADD_NEW_GAME_MESSAGE = "➕ Add a New Game"

class LoggingConstants:
    LOG_SEARCH = "User is searching for: {game_name}"
    LOG_ADD = "User is adding a new game: {game_name}"

def escape_markdown(text: str) -> str:
    """Экранирует текст для MarkdownV2 в Telegram, НЕ экранируя `*` для жирного шрифта."""
    escape_chars = r"_[]()~`>#+-=|{}.!"  # Убрали `*`, чтобы оставалось жирное выделение
    return re.sub(rf"([{re.escape(escape_chars)}])", r"\\\1", text)

# Описание кнопки `/start`
START_BUTTON_DESCRIPTION = escape_markdown(
    "🔄 Restart the bot and bring up the main menu.\n"
    "🎲 Find board games by name or photo, or add a new game to the database!"
)

# Приветственное сообщение
WELCOME_MESSAGE = escape_markdown(
    "👋 Welcome to *BoardGame Guru*!\n"
    "I can help you find and explain rules for board games 🎲✨\n\n"
    "Here's what I can do:\n"
    "📷 *Search by Photo* - Send a picture of a board game, and I'll identify it.\n"
    "🔤 *Search by Name* - Type a game name, and I'll find its rules.\n"
    "➕ *Add a New Game* - Help expand my database by adding a new game!\n\n"
    "Choose an option below 👇"
)

# Сообщение при нажатии "🔤 Search by Name"
REQUEST_GAME_NAME_MESSAGE = escape_markdown(
    "🔎 Please enter the name of the board game you want to find."
)

# Сообщение об игре
def game_info_message(game_name: str, game_info: str) -> str:
    return escape_markdown(f"*{game_name}*:\n{game_info}")

# Сообщение, если игра не найдена
def game_not_found_message(game_name: str) -> str:
    return escape_markdown(f"Sorry, I couldn't find *{game_name}* in my database. Try another name!")

# Сообщение при нажатии "📷 Search by Photo"
SEARCH_BY_PHOTO_MESSAGE = escape_markdown(
    "📷 Please send me a photo of the board game, and I'll try to recognize it!"
)

# Сообщение при нажатии "➕ Add a New Game"
ADD_NEW_GAME_MESSAGE = escape_markdown(
    "➕ Please send me the name and details of the game you want to add!"
)

ADD_GAME_REQUEST_MESSAGE = escape_markdown(
    "📝 Please enter the name of the board game you want to add."
)

ADD_GAME_SUCCESS_MESSAGE = escape_markdown(
    "✅ The game has been successfully added to the database!"
)

ADD_NEW_GAME = escape_markdown(
    "➕ Add a New Game"
)

FOUND_SIMILAR_GAMES = escape_markdown(
    "Found similar games. Select from the list or add a new one:"
)

SELCTED_GAME = "The game : {game_name} has been selected!"

ASK_QUESTION = escape_markdown(
    "Write your question about the game..."
)