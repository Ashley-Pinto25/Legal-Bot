from langchain_chroma import Chroma

from langchain_huggingface import HuggingFaceEmbeddings

VECTOR_DB_PATH = "vectorstores"

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def get_embedding_model():
    """
    Returns the embedding model.
    """
    return HuggingFaceEmbeddings(
        model_name=MODEL_NAME
    )


def load_vectorstore():
    """
    Loads the existing Chroma vector database.
    """
    embeddings = get_embedding_model()

    vectorstore = Chroma(
        persist_directory=VECTOR_DB_PATH,
        embedding_function=embeddings
    )

    return vectorstore