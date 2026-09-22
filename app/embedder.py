from sentence_transformers import SentenceTransformer
from chunker import load_documents, create_chunks

model = SentenceTransformer("all-MiniLM-L6-v2")

def create_embeddings(chunks):
    texts = [chunk["text"] for chunk in chunks]

    embeddings = model.encode(
        texts,
        show_progress_bar=True
    )
    return embeddings

if __name__ == "__main__":
    documents = load_documents()
    chunks = create_chunks(documents)
    embeddings = create_embeddings(chunks)

    print(f"\n Embeddings created \n Number of Embeddings :{len(embeddings)} \n Embedding dimensions: {len(embeddings[0])}")