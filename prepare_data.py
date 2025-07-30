import os
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import FAISS

# --- Configurations ---
PDF_PATH = "data/azure-databricks.pdf" # Path to PDF file
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2" # Embedding model name to be used
VECTOR_DB_PATH = "vector_db" # Folder where the vector database will be saved

# --- 1. Load the PDF ---
print(f"Loading PDF from: {PDF_PATH}...")
try:
    loader = PyPDFLoader(PDF_PATH)
    documents = loader.load()
    print(f"PDF loaded successfully! Total of {len(documents)} pages.")
except Exception as e:
    print(f"Error loading PDF: {e}")
    print("Please ensure the PDF file exists and the path is correct.")
    exit() # Stop the script if an error occurs

# --- 2. Split the text into chunks ---
print("Splitting text into chunks...")
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,       # Maximum size of each chunk (in characters)
    chunk_overlap=200,     # How many characters chunks can overlap (to maintain context)
    length_function=len    # Function to calculate chunk length
)
chunks = text_splitter.split_documents(documents)
print(f"Text split into {len(chunks)} chunks.")

# --- 3. Create Embeddings and Store in FAISS ---
print(f"Loading embedding model: {EMBEDDING_MODEL_NAME}...")
embeddings = SentenceTransformerEmbeddings(model_name=EMBEDDING_MODEL_NAME)

print("Generating embeddings and creating the FAISS vector database...")
# Create the vector database from the chunks and embeddings
vector_db = FAISS.from_documents(chunks, embeddings)

# --- 4. Save the Vector Database ---
print(f"Saving the vector database to: {VECTOR_DB_PATH}...")
vector_db.save_local(VECTOR_DB_PATH)
print("Vector database created and saved successfully!")
