"""
memory.py — Long-term memory management for Jarvis AI
Developed by: Jotiba Ugale
Purpose:
    Handles persistent memory using Pinecone Vector Database.
    Stores and retrieves embeddings of past user interactions for better context.
"""

import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer

# Load environment variables
load_dotenv()

# ============================================================
# ⚙️ Pinecone Configuration
# ============================================================
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = os.getenv("PINECONE_INDEX", "jarvis-memory")

if not PINECONE_API_KEY:
    raise ValueError("❌ Missing PINECONE_API_KEY in .env file")

# Initialize Pinecone client
pc = Pinecone(api_key=PINECONE_API_KEY)

# Create index if not existing
existing_indexes = [i.name for i in pc.list_indexes()]
if INDEX_NAME not in existing_indexes:
    print(f"🧠 Creating Pinecone index '{INDEX_NAME}'...")
    pc.create_index(
        name=INDEX_NAME,
        dimension=384,  # Matching MiniLM embedding size
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )

# Connect to index
index = pc.Index(INDEX_NAME)

# Initialize sentence embedding model
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# ============================================================
# 💾 Store Memory
# ============================================================
def store_memory(user_id: str, message: str, response: str):
    """
    Stores a user interaction (message + AI response) as a vector in Pinecone.

    Args:
        user_id (str): Unique identifier for the user.
        message (str): The user input.
        response (str): The AI model’s output.
    """
    try:
        text = f"User: {message}\nAI: {response}"
        emb = embedder.encode(text).tolist()
        unique_id = f"{user_id}-{abs(hash(text))}"

        index.upsert(vectors=[(unique_id, emb, {"text": text})])
    except Exception as e:
        print(f"[Error] Failed to store memory: {e}")


# ============================================================
# 🔍 Retrieve Memory
# ============================================================
def retrieve_memory(user_id: str, query: str, top_k: int = 3) -> str:
    """
    Retrieves the most relevant past interactions from Pinecone.

    Args:
        user_id (str): Unique identifier for the user.
        query (str): The new user query.
        top_k (int): Number of relevant matches to fetch.

    Returns:
        str: Concatenated string of relevant past context.
    """
    try:
        emb = embedder.encode(query).tolist()
        results = index.query(vector=emb, top_k=top_k, include_metadata=True)
        matches = getattr(results, "matches", [])

        if not matches:
            return ""

        # Extract past relevant text
        retrieved_context = "\n".join(
            [match.metadata.get("text", "") for match in matches]
        )
        return retrieved_context.strip()
    except Exception as e:
        print(f"[Error] Memory retrieval failed: {e}")
        return ""
