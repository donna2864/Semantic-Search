import chromadb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
client  = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection(name="documents")

def search(query, top_k=5):
    query_embedding = model.encode(query).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    return results

if __name__ == "__main__":
    query = input("Enter your query: ")
    results = search(query)

    print("\n Search Results: \n")
    for i in range(len(results["documents"][0])):
        print(f"Result: {i+1}")
        print("Source: ", results["metadatas"][0][i]["filename"])
        print("Text: ", results["documents"][0][i])
        print("Distance:", results["distances"][0][i])
        print()