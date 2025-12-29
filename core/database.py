import chromadb
from chromadb.config import Settings

def store_code_in_db(code_metadata, db_path="./chroma_db"):

    client = chromadb.PersistentClient(path=db_path)
    collection = client.get_or_create_collection(name="codebase_index")

    documents = [item['content'] for item in code_metadata]
    metadatas = [{
        "type": item['type'],
        "name": item['name'],
        "path": item['file'],
        } for item in code_metadata
    ]

    ids = [f"id_{i}_{item['name']}" for i, item in enumerate(code_metadata)]
    collection.upsert(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )

    print(f"Successfully indexed {len(documents)} code blocks into ChromaDB!")
    return collection

def search_code(collection, query, n_results=2):
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )

    for i in range(len(results['documents'][0])):
        print(f"--- Result {i+1} ---")
        print(f"File: {results['metadatas'][0][i]['file']}")
        print(f"Name: {results['metadatas'][0][i]['name']}")
        print(f"Snippet:\n{results['documents'][0][i][:200]}...")
        print("-" * 20)