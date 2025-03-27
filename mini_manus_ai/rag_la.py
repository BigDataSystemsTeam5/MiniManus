import os
from dotenv import load_dotenv
from langchain_core.tools import tool
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone


load_dotenv(r'C:\Users\Admin\Desktop\MS Data Architecture and Management\DAMG 7245 - Big Data Systems and Intelligence Analytics\Assignment 5 A\environment\access.env')

# Configure Pinecone Connection
pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))


index_name = "rag-index"
index = pc.Index(index_name)

# Embedding settings
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# Initialize the embedding model
embedding_model = SentenceTransformer(EMBEDDING_MODEL)

def format_rag_contexts(matches: list):
    contexts = []
    for x in matches:
        text = (
            f"Year: {x['metadata']['year']}\n"
            f"Quarter: {x['metadata']['quarter']}\n"
            f"Content: {x['metadata']['content']}\n"
        )
        contexts.append(text)
    context_str = "\n---\n".join(contexts)
    return context_str

@tool("rag_search_filter")
def rag_search_filter(query: str, year: int, quarter: int):
    """Finds information from Pinecone database using a natural language query
    and a specific year and quarter. Allows us to learn more details about a specific report."""

    year = 2024
    quarter = 4
    namespace = f"{year}-{quarter}"

    result = embedding_model.encode([query])
    embed_query = result.tolist()

    xc = index.query(vector=embed_query, top_k=5, include_metadata=True, namespace=namespace)
    context_str = format_rag_contexts(xc["matches"])
    return context_str
