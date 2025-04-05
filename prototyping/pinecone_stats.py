from pinecone import Pinecone

pc = Pinecone(api_key="")

# Delete a index
pc.delete_index(name="rag-index")

index = pc.Index("rag-index")
stats = index.describe_index_stats()
print(stats)
