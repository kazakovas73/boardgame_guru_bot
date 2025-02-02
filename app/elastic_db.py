from datetime import datetime
from elasticsearch import Elasticsearch
import os
import uuid
import logging
from dotenv import load_dotenv

load_dotenv()

# Подключение к Elasticsearch
ELASTIC_HOST = os.getenv("ELASTIC_HOST")
ELASTIC_PORT = os.getenv("ELASTIC_PORT")
ELASTIC_USER = os.getenv("ELASTIC_USER")
ELASTIC_PASSWORD = os.getenv("ELASTIC_PASSWORD")

es = Elasticsearch(
    f"http://{ELASTIC_HOST}:{ELASTIC_PORT}",
    basic_auth=(ELASTIC_USER, ELASTIC_PASSWORD),
    request_timeout=30
)

class IndexNames:
    TEXT_GAMES_INDEX = "text_game_index"
    RULES_PREFIX = "rules_"

def generate_deterministic_uuid(game_name: str):
    namespace = uuid.UUID("123e4567-e89b-12d3-a456-426614174000")  # Фиксированный namespace
    return str(uuid.uuid5(namespace, game_name))

# Создаём индекс, если его нет
def create_text_games_index():
    if not es.indices.exists(index=IndexNames.TEXT_GAMES_INDEX):
        es.indices.create(
            index=IndexNames.TEXT_GAMES_INDEX,
            body={
                "settings": {
                    "number_of_shards": 1,
                    "number_of_replicas": 0
                },
                "mappings": {
                    "properties": {
                        "game_id": {"type": "keyword"},
                        "game_name": {"type": "text"},
                        "vector": {"type": "dense_vector", "dims": 384},
                        "description": {"type": "text"},
                        "created_at": {"type": "date"}
                    }
                }
            }
        )
        logging.info(f"Индекс '{IndexNames.TEXT_GAMES_INDEX}' создан!")

async def create_rules_index(game_name):
    index_name = generate_deterministic_uuid(game_name)

    if not es.indices.exists(index=index_name):
        es.indices.create(
            index=index_name,
            body={
                "settings": {
                    "number_of_shards": 1,
                    "number_of_replicas": 0
                },
                "mappings": {
                    "properties": {
                        "rule_id": {"type": "keyword"},
                        "game_id": {"type": "keyword"},
                        "text": {"type": "text"},
                        "vector": {"type": "dense_vector", "dims": 384},
                        "created_at": {"type": "date"}
                    }
                }
            }
        )
        logging.info(f"Индекс '{index_name}' создан!")

# Функция добавления игры в Elasticsearch
async def elastic_add_game(game_name: str, vector: list):
    es.index(
        index=IndexNames.TEXT_GAMES_INDEX,
        body={
            "game_id": generate_deterministic_uuid(game_name),
            "game_name": game_name, 
            "vector": vector,
            "description": "",
            "created_at": datetime.now().isoformat() + "Z"
        }
    )
    logging.info(f"✅ Игра '{game_name}' добавлена в Elasticsearch!")

async def elastic_add_rules(game_name: str, rule: str, vector: list):
    es.index(
        index=generate_deterministic_uuid(game_name),
        body={
            "rule_id": generate_deterministic_uuid(rule),
            "game_id": generate_deterministic_uuid(game_name),
            "text": rule, 
            "vector": vector,
            "created_at": datetime.now().isoformat() + "Z"
        }
    )

# Функция поиска игры по вектору
def elastic_search_game_by_vector(vector: list, top_k=3):
    query = {
        "size": top_k,
        "query": {
            "script_score": {
                "query": {"match_all": {}},
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'vector') + 1.0",
                    "params": {"query_vector": vector}
                }
            }
        }
    }
    results = es.search(index=IndexNames.TEXT_GAMES_INDEX, body=query)
    hits = results["hits"]["hits"]

    return [hit["_source"]["game_name"] for hit in hits] if hits else []

def elastic_search_rule_by_vector(game_name, vector: list, top_k=5):
    index = generate_deterministic_uuid(game_name)
    query = {
        "size": top_k,
        "query": {
            "script_score": {
                "query": {"match_all": {}},
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'vector') + 1.0",
                    "params": {"query_vector": vector}
                }
            }
        }
    }
    results = es.search(index=index, body=query)
    hits = results["hits"]["hits"]

    logging.info(f"Search in {index} index")

    return [hit["_source"]["text"] for hit in hits] if hits else []