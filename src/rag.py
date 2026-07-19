from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings


#loading
def load_documents():
    loader = PyPDFDirectoryLoader("knowledge")
    return loader.load()


if __name__ == "__main__":

    documents = load_documents()

#chunking
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )

    chunks = splitter.split_documents(documents)

#embedding
    embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

#storing
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="vectorstores"
    )

    print(f"Documents : {len(documents)}")
    print(f"Chunks     : {len(chunks)}")
    print("\nVector Database Created Successfully!")

    

