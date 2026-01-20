import pickle
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

with open("backend/rag_store.pkl", "rb") as f:
    index, docs = pickle.load(f)

def retrieve_context(query, k=2):
    query_embedding = model.encode([query])
    distances, indices = index.search(query_embedding, k)
    retrieved_docs = [docs[i] for i in indices[0]]
    return {
        "context": "\n".join(retrieved_docs),
        "distances": distances[0].tolist()
    }
