from dotenv import load_dotenv
from chunking_evaluation.chunking import ClusterSemanticChunker
import os
import json
import tiktoken
import numpy as np
import pandas as pd
from chromadb.utils import embedding_functions
from chunking_evaluation.utils import openai_token_count


load_dotenv(r'environment\access.env')

def analyze_chunks(chunks, use_tokens=False):
    """
    Analyze a list of chunks to show statistics and overlaps.
    
    Args:
        chunks: List of text chunks
        use_tokens: Whether to analyze overlap by tokens instead of characters
    """
    # Print basic stats
    print("\nNumber of Chunks:", len(chunks))
    
    # Show examples of chunks
    if len(chunks) >= 2:
        print("\n", "="*50, f"Chunk #{len(chunks)//3}", "="*50)
        print(chunks[len(chunks)//3])
        print("\n", "="*50, f"Chunk #{2*len(chunks)//3}", "="*50)
        print(chunks[2*len(chunks)//3])
    
    # Calculate average chunk size
    if use_tokens:
        encoding = tiktoken.get_encoding("cl100k_base")
        chunk_sizes = [len(encoding.encode(chunk)) for chunk in chunks]
        print(f"\nAverage chunk size: {sum(chunk_sizes)/len(chunk_sizes):.1f} tokens")
        print(f"Min chunk size: {min(chunk_sizes)} tokens")
        print(f"Max chunk size: {max(chunk_sizes)} tokens")
    else:
        chunk_sizes = [len(chunk) for chunk in chunks]
        print(f"\nAverage chunk size: {sum(chunk_sizes)/len(chunk_sizes):.1f} characters")
        print(f"Min chunk size: {min(chunk_sizes)} characters")
        print(f"Max chunk size: {max(chunk_sizes)} characters")
    
    # Find overlaps if there are at least two chunks
    if len(chunks) >= 2:
        chunk1, chunk2 = chunks[len(chunks)//2], chunks[len(chunks)//2 + 1]
        
        if use_tokens:
            encoding = tiktoken.get_encoding("cl100k_base")
            tokens1 = encoding.encode(chunk1)
            tokens2 = encoding.encode(chunk2)
            
            # Find overlapping tokens
            for i in range(min(len(tokens1), 50), 0, -1):
                if tokens1[-i:] == tokens2[:i]:
                    overlap = encoding.decode(tokens1[-i:])
                    print("\n", "="*50, f"\nOverlapping text ({i} tokens):", overlap)
                    return
            print("\nNo token overlap found")
        else:
            # Find overlapping characters
            for i in range(min(len(chunk1), 200), 0, -1):
                if chunk1[-i:] == chunk2[:i]:
                    print("\n", "="*50, f"\nOverlapping text ({i} chars):", chunk1[-i:])
                    return
            print("\nNo character overlap found")



def save_chunks_to_json(chunks, strategy_name, output_dir="output"):
    """
    Save chunks to a JSON file for later analysis or reference.
    
    Args:
        chunks: List of text chunks
        strategy_name: Name of the chunking strategy
        output_dir: Directory to save the JSON file
        
    Returns:
        Path to the JSON file
    """
    # Create strategy directory if it doesn't exist
    strategy_dir = os.path.join(output_dir, strategy_name)
    os.makedirs(strategy_dir, exist_ok=True)
    
    # Create a JSON object with chunk information
    chunks_data = {
        "strategy": strategy_name,
        "chunk_count": len(chunks),
        "chunks": []
    }
    
    # Add each chunk with metadata
    for i, chunk in enumerate(chunks):
        encoder = tiktoken.get_encoding("cl100k_base")
        chunk_info = {
            "id": i,
            "text": chunk,
            "char_length": len(chunk),
            "token_length": len(encoder.encode(chunk))
        }
        chunks_data["chunks"].append(chunk_info)
    
    # Save to JSON file
    output_path = os.path.join(strategy_dir, "chunks.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(chunks_data, f, indent=2)
    
    print(f"Chunks saved to {output_path}")
    return output_path



# Load the sample document
with open(r"docling_output_md\NVIDIA.md", 'r', encoding='utf-8') as file:
    document = file.read()

# Get the total token count
encoding = tiktoken.get_encoding("cl100k_base")
tokens = encoding.encode(document)
print(f"Total document length: {len(tokens)} tokens")



# Check if OpenAI API key is set
api_key = os.environ.get("OPENAI_API_KEY")

if not api_key:
    print("Warning: OPENAI_API_KEY environment variable is not set. Skipping cluster semantic chunking strategies.")
else:
    # Set up output directory for cluster semantic chunking
    strategy_name = "cluster_chunking"
    #output_dir = setup_chunking_output(strategy_name)

    # Set up an embedding function
    embedding_function = embedding_functions.OpenAIEmbeddingFunction(
        api_key=api_key, 
        model_name="text-embedding-3-small"
    )
    
    # Using ClusterSemanticChunker from the chunking_evaluation library
    cluster_chunker = ClusterSemanticChunker(
        embedding_function=embedding_function, 
        max_chunk_size=300,  # Maximum chunk size in tokens
        length_function=openai_token_count
    )
    
    cluster_chunks = cluster_chunker.split_text(document)
    analyze_chunks(cluster_chunks, use_tokens=True)
    
    # Save chunks to JSON
    save_chunks_to_json(cluster_chunks, strategy_name)