import chromadb
from fixed_chunker import load_documents, create_fixed_chunks
from embedder import create_embeddings


client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection( name="fixed_documents")


def store_fixed_documents():
    documents = load_documents()
    chunks = create_fixed_chunks(documents)
    embeddings = create_embeddings(chunks)

    ids = [f"fixed_chunk_{i}" for i in range(len(chunks))]
    texts = [chunk["text"] for chunk in chunks ]
    metadatas = [{ "filename": chunk["filename"]} for chunk in chunks ]

    collection.add(
        ids=ids,
        documents=texts,
        embeddings=embeddings.tolist(),
        metadatas=metadatas
    )

    print("Fixed-size documents stored successfully!")
    print("Total fixed chunks in database:", collection.count())


if __name__ == "__main__":
    store_fixed_documents()