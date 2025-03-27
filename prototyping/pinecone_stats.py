from pinecone import Pinecone

pc = Pinecone(api_key="pcsk_2nvmif_P9k6nG7RFt6fvwKZvxK2ywKHSfHWPqvN1r4yw61EyvNj18kFHcZN7CAfu7uiF82")
index = pc.Index("rag-index")
stats = index.describe_index_stats()
print(stats)
