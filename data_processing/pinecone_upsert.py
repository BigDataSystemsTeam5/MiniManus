import json
import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
import time


def upsert_pinecone(embed_json, year, quarter):

    load_dotenv(r'C:\Users\Admin\Desktop\MS Data Architecture and Management\DAMG 7245 - Big Data Systems and Intelligence Analytics\Assignment 5 A\environment\access.env')

    # Configure Pinecone Connection
    pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))

    #with open(embed_json, "r", encoding="utf-8") as file:
        #content = embed_json.read()
    data = json.loads(embed_json)

    # Delete a index
    pc.delete_index(name="rag-index")

    # Create a index with integrated embedding
    index_name = "rag-index"

    if not pc.has_index(index_name):
        pc.create_index(
            name=index_name,
            dimension=384,  # Critical: matches MiniLM-L6-v2 output
            spec = ServerlessSpec(
                cloud='aws', 
                region='us-east-1'
            )
        )

    print(f'The list of indices in Pinecone Database: {pc.list_indexes()}')

    index = pc.Index(index_name)

    # Upsert the records into a namespace
    index.upsert(namespace=f"{year}-{quarter}", vectors=data)
    
    time.sleep(20)

    # View stats for the index
    stats = index.describe_index_stats()

    return stats



#embed_json = r"C:\Users\Admin\Desktop\MS Data Architecture and Management\DAMG 7245 - Big Data Systems and Intelligence Analytics\Assignment 5 A\data_processing\chunk_embed_output\recursive_chunking_with_overlap\chunks_2024_4.json"
#result = upsert_pinecone(embed_json, 2024, 4)
#print(result)