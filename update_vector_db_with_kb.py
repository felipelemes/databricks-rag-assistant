import os
import json
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import FAISS

# --- Configurations ---
# Folder where scraped JSON articles are saved by scrape_kb.py
SCRAPED_ARTICLES_DIR = "scraped_kb_articles"
# Path to your existing FAISS vector database (from PDF)
VECTOR_DB_PATH = "vector_db"
# Same embedding model name used in prepare_data.py
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

# --- 1. Load Scraped Articles from JSON ---
def load_scraped_articles(directory):
    """
    Loads articles saved as JSONs and converts them into LangChain Documents.
    Combines title and content to form 'page_content'.
    """
    articles = []
    print(f"Searching for JSON articles in folder: {directory}")
    if not os.path.exists(directory):
        print(f"Warning: Scraped articles directory not found: {directory}")
        return articles

    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            filepath = os.path.join(directory, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Combine title and content for the Document's page_content
                    full_content = f"Title: {data.get('title', 'N/A')}\n\n{data.get('content', '')}"
                    articles.append(Document(
                        page_content=full_content,
                        metadata={"source": data.get('url', filename), "title": data.get('title', '')}
                    ))
            except Exception as e:
                print(f"Error loading or processing file {filename}: {e}")
    print(f"Loaded {len(articles)} scraped KB articles.")
    return articles

# --- 2. Split New Documents into Chunks ---
def split_documents_into_chunks(documents):
    """
    Splits a list of LangChain Documents into smaller chunks.
    Uses the same chunk_size and chunk_overlap settings as the PDF processing.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Documents split into {len(chunks)} new chunks.")
    return chunks

# --- Main Vector Database Update Logic ---
if __name__ == "__main__":
    print("Starting the process of updating the vector database with KB articles...")

    # Load the embedding model (the same one used for the PDF)
    print(f"Loading embedding model: {EMBEDDING_MODEL_NAME}...")
    embeddings = SentenceTransformerEmbeddings(model_name=EMBEDDING_MODEL_NAME)
    print("Embedding model loaded.")

    # 1. Load the scraped JSON articles
    new_documents = load_scraped_articles(SCRAPED_ARTICLES_DIR)

    if not new_documents:
        print("No new articles found in the scraped data folder to add to the database. Exiting.")
        exit()

    # 2. Split the new documents into chunks
    new_chunks = split_documents_into_chunks(new_documents)

    # 3. Load the existing FAISS vector database (from the PDF)
    print(f"Loading existing FAISS vector database from: {VECTOR_DB_PATH}...")
    try:
        # Ensure the 'vector_db' was created with 'prepare_data.py' first
        vector_db = FAISS.load_local(VECTOR_DB_PATH, embeddings, allow_dangerous_deserialization=True)
        print("Existing FAISS vector database loaded successfully.")
    except Exception as e:
        print(f"Error loading existing FAISS vector database: {e}")
        print("Please ensure the 'vector_db' database was created with 'prepare_data.py' BEFORE running this script.")
        exit()

    # 4. Add the new chunks to the existing database
    print(f"Adding {len(new_chunks)} new chunks to the FAISS database...")
    # The add_documents method adds the new documents and their embeddings to the existing index
    vector_db.add_documents(new_chunks)
    print("New chunks added to the database.")

    # 5. Save the updated FAISS vector database
    print(f"Saving the updated FAISS vector database to: {VECTOR_DB_PATH}...")
    vector_db.save_local(VECTOR_DB_PATH)
    print("FAISS vector database updated and saved successfully!")
    print("\nNow, run your Streamlit application ('streamlit run app.py') to see your assistant with the new knowledge!")