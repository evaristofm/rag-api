from app.services.vector_store import VectorStoreService

with open(file="profile.txt", mode="r", encoding="utf-8") as f:
    text = f.read()

chunks = [chunk.strip() for chunk in text.split("\n\n") if chunk.strip()]

print(f"Loaded {len(chunks)} chunks from profile.txt")

vector_store = VectorStoreService()

vector_store.add_documents(
    ids=[f"chunk{i}" for i in range(len(chunks))],
    documents=chunks,
    metadatas=[{"source": "profile", "chunk_index": i} for i in range(len(chunks))],
)

print(f"Added {len(chunks)} chunks to the 'personal_profile' collection.")
print("Knowledge base built successfully!")
