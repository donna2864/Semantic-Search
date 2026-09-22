import chromadb
from chunker import load_documents, create_chunks
from embedder import create_embeddings

client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_or_create_collection(name="documents")

def store_documents():
    documents = load_documents()
    chunks = create_chunks(documents)
    embeddings = create_embeddings(chunks)

    ids = [f"chunk_{i}" for i in range(len(chunks))]
    texts = [chunk["text"] for chunk in chunks]
    metadatas = [{
        "filename":chunk["filename"]
    } for chunk in chunks]

    collection.add(
        ids=ids,
        documents=texts,
        embeddings=embeddings.tolist(),
        metadatas=metadatas
    )

    print(f"\n Documents stored successfully! \n Total chunks in database: {collection.count()}")

if __name__ == "__main__":
    store_documents()