import chromadb
from sentence_transformers import SentenceTransformer
from evaluation_data import EVALUATION_QUERIES
from search import search

model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection(name="documents")

def calculate_precision_at_5():
    total_precision = 0
    for item in EVALUATION_QUERIES:
        query = item["query"]
        relevant_source = item["relevant_source"]
        results = search(query, top_k=5)

        sources = [
            metadata['filename'] for metadata in results['metadatas'][0]
        ]

        relavent_results = sources.count(relevant_source)
        precision = relavent_results/5
        total_precision += precision

        print("\n Query: ", query)
        print("Expected: ", relevant_source)
        print("Retrieved: ", sources)
        print("Precision@5: ", precision)

    average_precision = total_precision/len(EVALUATION_QUERIES)
    print("-"*10)
    print("Overall Precision@5: ", round(average_precision,2))
    print("-"*10)

if __name__ == "__main__":
    calculate_precision_at_5()