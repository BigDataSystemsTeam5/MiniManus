#from langchain_huggingface import HuggingFaceEmbeddings
#import numpy as np
from sentence_transformers import SentenceTransformer
#from langchain_pinecone import Pinecone  # New official interface
from pinecone import Pinecone, ServerlessSpec, PodSpec
from langchain_pinecone import PineconeVectorStore


def upsert_pinecone(chunks):

    # Configure Pinecone Connection
    pc = Pinecone(api_key="pcsk_2nvmif_P9k6nG7RFt6fvwKZvxK2ywKHSfHWPqvN1r4yw61EyvNj18kFHcZN7CAfu7uiF82")

    print(pc.list_indexes())

    # Initialize Embeddings Model (384 dimensions)
    #embeddings = HuggingFaceEmbeddings(
    #    model_name="sentence-transformers/all-MiniLM-L6-v2",
    #    model_kwargs={'device': 'cpu'},  # or 'cuda' for GPU
    #    encode_kwargs={'normalize_embeddings': True}
    #)


    # Create/Connect Index with 384 dimensions
    index_name = "rag-index"
    pc.create_index(
        name=index_name,
        dimension=384,  # Critical: matches MiniLM-L6-v2 output
        metric="cosine",
        #spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        spec=PodSpec(environment="us-east-1-aws", metadata_config={"indexed": ["year", "quarter"]})
    )

    print(pc.list_indexes())
    index = pc.Index(index_name)

    # Embedding settings
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"

    # Initialize the embedding model
    embeddings = SentenceTransformer(EMBEDDING_MODEL)

    # Store Documents with Metadata
    #vector_store = PineconeVectorStore.from_documents(
    vector_store = PineconeVectorStore(
        documents=chunks,  # List of Document objects with metadata
        embedding=embeddings,
        index_name=index_name
    )

    index_stats = index.describe_index_stats()
    return f"Total vectors: {index_stats['total_vector_count']}"


chunks = r"C:\Users\Admin\Desktop\MS Data Architecture and Management\DAMG 7245 - Big Data Systems and Intelligence Analytics\Assignment 5 A\data_processing\chunk_output\recursive_chunking_with_overlap\chunks_2024_4.json"
result = upsert_pinecone(chunks)
print(result)



#def embeddings_check(chunks):
#    if chunks:
#        # Create embeddings for the first 3 chunks
#        sample_chunks = chunks[:min(3, len(chunks))]
#        embeddings = upsert_pinecone(sample_chunks)
#
#        # Print embedding information
#        print(f"Embedding dimensions: {embeddings.shape}")
#        print(f"Sample embedding (first 10 values): {embeddings[0][:10]}")
#
#        # Calculate similarity between the first two chunks if possible
#        if len(embeddings) >= 2:
#            # Using cosine similarity: dot product of normalized vectors
#            def cosine_similarity(v1, v2):
#                return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
#
#            sim = cosine_similarity(embeddings[0], embeddings[1])
#            print(f"\nSimilarity between first two chunks: {sim:.4f}")
#    else:
#        print("No chunks to embed")



#def chunks_analyze():
#    
#    if chunks:
#        # Add chunks to the collection
#        num_added = add_chunks_to_collection(chunks, url)
#        print(f"Added {num_added} chunks to the collection")
#    
#        # Get the collection and check count
#        collection = get_or_create_collection()
#        count = collection.count()
#        print(f"Total documents in collection: {count}")
#    else:
#        print("No chunks to add")