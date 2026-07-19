from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

loader = PyPDFDirectoryLoader("knowledge")
#loads the entire directory of PDF files located in the "knowledge" folder. It creates an instance of the PyPDFDirectoryLoader class and initializes it with the path to the directory containing the PDF files.

documents = loader.load()
#loading

print(f"Total Documents Loaded : {len(documents)}")

print("\n==============================")
print("First Document")
print("==============================")

print("\nPage Content:\n")
print(documents[0].page_content[:500])  # First 500 characters

print("\nMetadata:\n")
print(documents[0].metadata)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = text_splitter.split_documents(documents)
print(f"Original Documents : {len(documents)}")
print(f"Chunks Created     : {len(chunks)}")

print("\n========== First Chunk ==========\n")

print(chunks[0].page_content)

print("\nMetadata:\n")

print(chunks[0].metadata)
