import os
import pickle
import faiss
from sentence_transformers import SentenceTransformer 

model = SentenceTransformer('all-MiniLM-L6-v2')
# embedding model

docs = []

for file in os.listdir("knowledge_base"):
    with open(f"knowledge_base/{file}", "r") as f:
        docs.append(f.read())

embeddings = model.encode(docs)
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

with open("backend/rag_store.pkl", "wb") as f:
    pickle.dump((index, docs), f)

print("✅ Knowledge base indexed")