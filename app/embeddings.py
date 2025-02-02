from sentence_transformers import SentenceTransformer

class EmbeddingModel:
    _instance = None

    @classmethod
    def get_model(cls):
        """Загружает модель один раз"""
        if cls._instance is None:
            cls._instance = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        return cls._instance

def get_text_embedding(model, text: str) -> list:
    """Генерирует эмбеддинг для текста, используя единственный экземпляр модели"""
    model = model.get_model()
    return model.encode(text).tolist()