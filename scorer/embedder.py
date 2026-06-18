from sentence_transformers import SentenceTransformer
from config import EMBEDDING_MODEL

model = SentenceTransformer(EMBEDDING_MODEL)


def get_embedding(text):
    if not text or not text.strip():
        return None
    return model.encode(text)