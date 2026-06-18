from scorer.embedder import get_embedding
import numpy as np

text1 = "Python developer with machine learning experience"
text2 = "Machine learning engineer skilled in Python"
text3 = "Civil engineer specializing in structural design"

emb1 = get_embedding(text1)
emb2 = get_embedding(text2)
emb3 = get_embedding(text3)

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

print("Embedding shape:", emb1.shape)
print("\nSimilarity (Python dev vs ML engineer):", cosine_similarity(emb1, emb2))
print("Similarity (Python dev vs Civil engineer):", cosine_similarity(emb1, emb3))