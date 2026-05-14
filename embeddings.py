import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from loguru import logger

# Initialize vector store directory
PERSIST_DIRECTORY = os.path.join(os.path.dirname(__file__), '..', 'vector_store')

def get_vector_store():
    """
    Initializes and returns the ChromaDB vector store.
    """
    if not os.getenv("OPENAI_API_KEY"):
        logger.warning("OPENAI_API_KEY not found. Vector store might fail if embeddings are needed.")

    embeddings = OpenAIEmbeddings()
    vector_store = Chroma(
        collection_name="crypto_insights",
        embedding_function=embeddings,
        persist_directory=PERSIST_DIRECTORY
    )
    return vector_store

def embed_documents(texts: list, metadatas: list = None):
    """
    Embeds a list of texts and saves them into ChromaDB.
    """
    try:
        vector_store = get_vector_store()
        vector_store.add_texts(texts=texts, metadatas=metadatas)
        # In newer chromadb versions with langchain, add_texts automatically persists.
        logger.info(f"Successfully embedded {len(texts)} documents.")
    except Exception as e:
        logger.error(f"Failed to embed documents: {e}")
