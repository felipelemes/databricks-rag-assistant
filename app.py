import streamlit as st
import os
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import ChatPromptTemplate

# --- Path Configurations ---
VECTOR_DB_PATH = "vector_db"
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

# --- 1. Load Resources (Vector Database and Embedding Model) ---
# @st.cache_resource loads these components only once when the Streamlit app starts
@st.cache_resource
def load_resources():
    st.spinner("Loading embedding model...")
    print(f"Loading embedding model: {EMBEDDING_MODEL_NAME}...")
    embeddings = SentenceTransformerEmbeddings(model_name=EMBEDDING_MODEL_NAME)
    print("Embedding model loaded.")

    st.spinner("Loading vector database...")
    print(f"Loading FAISS vector database from: {VECTOR_DB_PATH}...")
    # allow_dangerous_deserialization=True is needed for FAISS.load_local
    # It's safe to use if you generated the database yourself.
    vector_db = FAISS.load_local(VECTOR_DB_PATH, embeddings, allow_dangerous_deserialization=True)
    print("Vector database loaded.")

    return embeddings, vector_db

embeddings, vector_db = load_resources()

# --- 2. Load and Configure the OpenAI LLM (GPT-4o) ---
openai_api_key = os.getenv("OPENAI_API_KEY")

if openai_api_key:
    try:
        llm = ChatOpenAI(
            temperature=0.85, # Controls creativity/randomness (0.0 to 1.0)
            api_key=openai_api_key,
            model_name="gpt-4o",
            model_kwargs={"top_p": 0.9} # Controls diversity of output
        )
        st.success("OpenAI model (gpt-4o) loaded successfully!")
    except Exception as e:
        st.error(f"Error initializing OpenAI model. Check your API key, "
                 f"model name, and plan/quotas: {e}")
        st.stop() # Stop the app if LLM cannot be initialized
else:
    st.error("OpenAI API Key (OPENAI_API_KEY) not found in environment variables.")
    st.stop() # Stop the app if API key is not found

# --- 3. Define the System Prompt for Assistant Behavior ---
SYSTEM_PROMPT_TEMPLATE = """
You are a friendly, experienced, and patient study tutor specializing in Databricks.
Your goal is to help the user deeply understand topics from Databricks documentation to prepare for Databricks certifications.

Follow these guidelines:
1.  **Always respond in the same language as the user's question.** If the question is in Portuguese, reply in Portuguese. If it's in English, reply in English.
2.  **Explain clearly and concisely:** Use accessible language and avoid unnecessary jargon where possible.
3.  **Go beyond simple retrieval:** Do not just reproduce information. Interpret it, reorganize it, and present it in a didactic way.
4.  **Provide practical examples:** If appropriate, create small examples or analogies to illustrate the concept within the context of Databricks or data engineering scenarios.
5.  **Maintain an encouraging and motivating tone:** Encourage the user in their learning.
6.  **Use the provided "Context Documents" to answer the question.** Prioritize information from these documents.
7.  **If the answer is not in the context documents, be honest:** State that you could not find the information and suggest the user search other sources or rephrase the question. Do not invent information.
8.  Format your responses legibly, using lists, bold text, or code blocks when appropriate.

Context Documents:
{context}

User Question:
{question}
"""

# Create a ChatPromptTemplate from the System Prompt
qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT_TEMPLATE),
        ("human", "{question}") # Where the user's question will be inserted
    ]
)

# --- 4. Configure the RAG Chain (RetrievalQA) ---
print("Configuring the RAG chain...")
qa_chain = RetrievalQA.from_chain_type(
    llm=llm, # <-- THIS IS THE CORRECTED LINE!
    chain_type="stuff", # 'stuff' strategy puts all retrieved documents directly into the LLM's prompt
    retriever=vector_db.as_retriever(search_kwargs={"k": 4}), # Configure FAISS as the retriever
                                                              # k=4 means it retrieves the 4 most relevant chunks
    return_source_documents=True, # Optional: returns the documents that were used for the answer
    chain_type_kwargs={"prompt": qa_prompt} # Pass the custom prompt to the chain
)
print("RAG chain configured.")

# --- 5. Streamlit Interface ---
st.set_page_config(
    page_title="📚 Databricks Study Assistant with RAG",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Create columns layout
col1, col2 = st.columns([3, 1])

with col1:
    st.title("📚 Databricks Study Assistant with RAG") # Updated title text

    # Updated objective description
    st.markdown("""
        This assistant is designed to provide you with precise, context-aware answers directly sourced from the official Azure Databricks documentation.
        It aims to significantly aid your studies for Databricks certifications and streamline the process of resolving technical challenges by offering a more fluid and natural consultation experience.
    """)

    # Updated context description
    st.markdown("""
        This assistant's knowledge base is built upon the official Azure Databricks documentation
        ([https://learn.microsoft.com/en-us/azure/databricks/](https://learn.microsoft.com/en-us/azure/databricks/))
        and the official Databricks Azure Knowledge Base
        ([https://kb.databricks.com/](https://kb.databricks.com/)).
    """)

    user_query = st.text_input(
        "Your question about Databricks documentation:",
        placeholder="Ex: How to configure Auto Loader in Databricks?"
    )

    if st.button("Get Answer", type="primary"):
        if user_query:
            with st.spinner("Searching and generating response..."):
                try:
                    response = qa_chain({"query": user_query})
                    st.subheader("Answer:")
                    st.markdown(response["result"]) # Use markdown for formatting the response

                    st.subheader("Source Documents:")
                    if response["source_documents"]:
                        for i, doc in enumerate(response["source_documents"]):
                            st.write(f"**Page/Source {i+1}:**")
                            st.info(doc.page_content) # Content of the chunk
                            if 'page' in doc.metadata: # If the PDF loader added the page number
                                st.write(f"*(Page: {doc.metadata['page'] + 1})*") # +1 because it's 0-based
                            st.markdown("---")
                    else:
                        st.info("No relevant source documents found for this question.")
                except Exception as e:
                    st.error(f"An error occurred while processing your question: {e}")
                    st.info("Please check your OpenAI API key, model name, and plan/quotas.")
        else:
            st.warning("Please type your question before submitting.")

with col2:
    st.markdown("<br><br>", unsafe_allow_html=True)  # Espaço para baixo
    st.markdown('<div style="text-align: right;">', unsafe_allow_html=True)
    st.image("donate.png", width=180)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
st.caption("Developed by you, with LangChain, Streamlit, and LLMs.")