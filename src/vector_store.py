import os

SYSTEM_CA = "/etc/ssl/certs/ca-certificates.crt"

os.environ["REQUESTS_CA_BUNDLE"] = SYSTEM_CA
os.environ["SSL_CERT_FILE"] = SYSTEM_CA
os.environ["CURL_CA_BUNDLE"] = SYSTEM_CA

print("Using certificate bundle:", SYSTEM_CA)

import chromadb
from sentence_transformers import SentenceTransformer

from src.document_loader import load_policy_documents



# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

EMBEDDING_MODEL = "BAAI/bge-large-en-v1.5"
COLLECTION_NAME = "airport_policies"
CHROMA_PATH = "chroma_db"


# ---------------------------------------------------------
# Embedding Model
# ---------------------------------------------------------

def load_embedding_model():
    """
    Load the BGE-large embedding model.
    """

    model = SentenceTransformer(EMBEDDING_MODEL)

    return model


# ---------------------------------------------------------
# Chunking
# ---------------------------------------------------------

def chunk_text(text, chunk_size=700, overlap=100):
    """
    Split text into overlapping character-based chunks.
    """

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break

        start = end - overlap

    return chunks


# ---------------------------------------------------------
# ChromaDB
# ---------------------------------------------------------

def get_chroma_collection():
    """
    Create or retrieve the persistent ChromaDB collection.
    """

    client = chromadb.PersistentClient(path=CHROMA_PATH)

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={
            "description": "Airport operations policy knowledge base"
        }
    )

    return collection


# ---------------------------------------------------------
# Build Vector Store
# ---------------------------------------------------------

def build_vector_store():

    print("Loading policy documents...")

    documents = load_policy_documents()

    print(f"Loaded {len(documents)} documents.")

    print("Loading embedding model...")

    model = load_embedding_model()

    print("Connecting to ChromaDB...")

    collection = get_chroma_collection()

    # Avoid duplicate documents when script is run multiple times
    existing = collection.get()

    existing_ids = set(existing["ids"])

    document_count = 0
    chunk_count = 0

    for document in documents:

        source = document["metadata"]["source"]

        chunks = chunk_text(document["text"])

        document_count += 1

        for chunk_number, chunk in enumerate(chunks):

            chunk_id = f"{source}_{chunk_number}"

            # Skip already indexed chunks
            if chunk_id in existing_ids:
                continue

            embedding = model.encode(
                chunk,
                normalize_embeddings=True
            ).tolist()

            collection.add(
                ids=[chunk_id],
                documents=[chunk],
                embeddings=[embedding],
                metadatas=[
                    {
                        "source": source,
                        "airport": document["metadata"]["airport"],
                        "policy_type": document["metadata"]["policy_type"],
                        "chunk_number": chunk_number
                    }
                ]
            )

            chunk_count += 1

    print(f"Documents processed: {document_count}")
    print(f"New chunks added: {chunk_count}")
    print(f"Total chunks in database: {collection.count()}")

    return collection


# ---------------------------------------------------------
# Semantic Search
# ---------------------------------------------------------

def retrieve_documents(query, top_k=5):

    model = load_embedding_model()

    collection = get_chroma_collection()

    query_embedding = model.encode(
        query,
        normalize_embeddings=True
    ).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    retrieved_documents = []

    for i in range(len(results["documents"][0])):

        retrieved_documents.append(
            {
                "text": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "distance": results["distances"][0][i]
            }
        )

    return retrieved_documents
