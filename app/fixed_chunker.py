from pathlib import Path

DOCUMENTS_DIR = Path('documents')

def load_documents():
    documents = []

    for file_path in DOCUMENTS_DIR.glob('*.txt'):
        text = file_path.read_text(encoding='utf-8')
        documents.append({
            "filename":file_path.name,
            "text": text
        })
    return documents

def create_fixed_chunks(documents, chunk_size=40):
    chunks = []

    for document in documents:
        words = document['text'].split()

        for i in range(0, len(words), chunk_size):
            chunk_words = words[i:i+chunk_size]
            chunks.append({
                "filename":document["filename"],
                "text":" ".join(chunk_words)
            })
    return chunks

if __name__ == "__main__":
    documents = load_documents()
    chunks = create_fixed_chunks(documents)

    print("Documents loaded: ", len(documents))
    print("Fixed chunks created: ", len(chunks))

    for i, chunk in enumerate(chunks):
        print(f"\n Chunk_{i+1}")
        print("Source: ", chunk["filename"])
        print("Test: ", chunk["text"])