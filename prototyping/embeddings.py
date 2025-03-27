import numpy as np
from sentence_transformers import SentenceTransformer

# Embedding settings
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# Initialize the embedding model
embedding_model = SentenceTransformer(EMBEDDING_MODEL)

def embed_chunks(chunks):
    """
    Create embeddings for a list of text chunks.
    
    Args:
        texts (list): List of text strings to embed
        
    Returns:
        numpy.ndarray: Array of embeddings
    """
    embeddings = embedding_model.encode(chunks)
    return embeddings

def embeddings_check(chunks):
    if chunks:
        # Create embeddings for the first 3 chunks
        sample_chunks = chunks[:min(3, len(chunks))]
        embeddings = embed_chunks(sample_chunks)

        # Print embedding information
        print(f"Embedding dimensions: {embeddings.shape}")
        print(f"Sample embedding (first 10 values): {embeddings[0][:10]}")

        # Calculate similarity between the first two chunks if possible
        if len(embeddings) >= 2:
            # Using cosine similarity: dot product of normalized vectors
            def cosine_similarity(v1, v2):
                return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

            sim = cosine_similarity(embeddings[0], embeddings[1])
            print(f"\nSimilarity between first two chunks: {sim:.4f}")
    else:
        print("No chunks to embed")