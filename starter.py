import os
from dotenv import load_dotenv
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
)

# Load environment variables from .env file
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Define storage directory
PERSIST_DIR = "./storage"
# Ensure the directory exists
os.makedirs(PERSIST_DIR, exist_ok=True)

# Check if the necessary persistence files exist
docstore_path = os.path.join(PERSIST_DIR, "docstore.json")
index_store_path = os.path.join(PERSIST_DIR, "index_store.json")
vector_store_path = os.path.join(PERSIST_DIR, "vector_store.json")

if not (os.path.exists(docstore_path) and os.path.exists(index_store_path) and os.path.exists(vector_store_path)):
    # Create and persist the index if the files are missing
    print("No existing index found. Creating a new one...")
    documents = SimpleDirectoryReader("./data/paul_graham/").load_data()
    index = VectorStoreIndex.from_documents(documents)
    index.storage_context.persist(persist_dir=PERSIST_DIR)
    print("Index has been successfully created and persisted.")
else:
    # Load the existing index
    print("Existing index found. Loading...")
    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    index = load_index_from_storage(storage_context)
    print("Existing Index loaded...")


# either way, i can now query the index
query_engine = index.as_query_engine()
response = query_engine.query("What did the author do growing up?")
print(response)
