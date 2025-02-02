import os
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from app.constants import escape_markdown
from app.elastic_db import elastic_search_rule_by_vector
from app.embeddings import get_text_embedding

async def _search_rules(message: Message, state: FSMContext, model):
    emb = get_text_embedding(model, message.text)

    data = await state.get_data()

    similar_rules = elastic_search_rule_by_vector(data['game_name'], emb)

    if similar_rules:
        for rule in similar_rules:
            await message.answer(escape_markdown(rule))
    else:
        await message.answer("No rules found for your query")