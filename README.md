---
title: Databricks RAG Study Assistant
emoji: 📚
colorFrom: blue
colorTo: green
sdk: streamlit
sdk_version: 1.47.1 # IMPORTANT: Ensure this matches your streamlit version in requirements.txt
app_file: app.py
pinned: false
---

# 📚 Databricks Study Assistant with RAG

## English

### Project Overview

This is an AI-powered Retrieval Augmented Generation (RAG) system designed to act as a specialized study tutor and technical consultant for Azure Databricks documentation. It aims to provide quick, precise, and context-aware answers directly from official Databricks resources, significantly enhancing study efficiency for certifications and streamlining daily technical problem-solving.

This project aims not only to consolidate my learning in Machine Learning and data engineering but also to create a practical and accessible tool for the community.

### Technical Details

* **Objective:** Interactive consultation assistant for Azure Databricks documentation (Data Engineer Associate Certification & professional use).
* **Knowledge Corpus:**
    * Official Databricks Documentation (approx. 17,800 pages, PDF).
    * Official Databricks Knowledge Base (kb.databricks.com, +900 Q&A articles via web scraping).
* **Content Processing:**
    * **Chunking:** Text split into chunks of 1000 characters with 200 characters overlap.
    * **Embeddings:** `all-MiniLM-L6-v2` model (multilingual, for semantic similarity in Portuguese/English).
    * **Vector Database:** FAISS (Facebook AI Similarity Search) for low-latency vector indexing and retrieval.
* **Large Language Model (LLM):** OpenAI GPT-4o (Generates precise, contextualized, and friendly answers, guided by prompt engineering).
* **Interface:** Streamlit (interactive web application).
* **Multilingual Capability:** Supports questions in Portuguese, based on English documentation, and replies in the query's language.

### Setup and Running Locally

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/YOUR_GITHUB_USERNAME/databricks-rag-study-assistant.git](https://github.com/YOUR_GITHUB_USERNAME/databricks-rag-study-assistant.git)
    cd databricks-rag-study-assistant
    ```
2.  **Create and Activate Virtual Environment:**
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```
3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  4.  **Download Databricks Documentation PDF:**
    Download the `azure-databricks.pdf` file (the 17,800-page official documentation) from the link below and place it into the `data/` directory of this project.
    [**Download Azure Databricks Official Documentation PDF (540MB)**](https://drive.google.com/file/d/1AhsUstnfmnvA9vBkPvE5S9GO06gxXa-N/view?usp=sharing)

    *Note: This file is too large to be hosted directly on GitHub, hence the external link.*
    You can also download the latest Azure Databricks documentation directly from the official website. Simply access the link [**HERE**](https://learn.microsoft.com/en-us/azure/databricks/), scroll to the bottom of the page, locate the "Download PDF" button in the lower-left corner, and click it. Make sure to save the file as "azure-databricks.pdf".
5.  **Prepare the Vector Database (PDF):**
    This script processes the PDF and creates the initial FAISS vector database.
    ```bash
    python prepare_data.py
    ```
6.  **Scrape Databricks Knowledge Base Articles:**
    This script scrapes articles from the Databricks KB and saves them as JSONs.
    ```bash
    python scrape_kb.py
    ```
7.  **Update Vector Database with KB Articles:**
    This script integrates the scraped articles into your existing FAISS vector database.
    ```bash
    python update_vector_db_with_kb.py
    ```
8.  **Set OpenAI API Key:**
    Obtain your OpenAI API Key from [platform.openai.com](https://platform.openai.com/api-keys) and set it as an environment variable in your terminal session:
    ```bash
    # Windows (PowerShell)
    $env:OPENAI_API_KEY="YOUR_API_KEY"
    # macOS/Linux
    export OPENAI_API_KEY="YOUR_API_KEY"
    ```
9.  **Run the Streamlit Application:**
    ```bash
    streamlit run app.py
    ```

---

## Português

### Visão Geral do Projeto

Este é um sistema de Geração Aumentada por Recuperação (RAG) baseado em IA, projetado para atuar como um tutor de estudos especializado e consultor técnico para a documentação do Azure Databricks. Seu objetivo é fornecer respostas rápidas, precisas e contextualizadas diretamente de recursos oficiais do Databricks, aprimorando significativamente a eficiência do estudo para certificações e simplificando a resolução de problemas técnicos diários.

Este projeto visa não apenas consolidar meu aprendizado em Machine Learning e engenharia de dados, mas também criar uma ferramenta prática e acessível para a comunidade.

### Detalhes Técnicos

* **Objetivo:** Assistente de consulta interativa para documentação do Azure Databricks (Certificação Data Engineer Associate e uso profissional).
* **Corpus de Conhecimento:**
    * Documentação Oficial do Databricks (aprox. 17.800 páginas, PDF).
    * Knowledge Base Oficial do Databricks (kb.databricks.com, +900 artigos de Q&A via web scraping).
* **Processamento de Conteúdo:**
    * **Chunking:** Texto dividido em pedaços (chunks) de 1000 caracteres com 200 caracteres de sobreposição.
    * **Embeddings:** Modelo `all-MiniLM-L6-v2` (multilíngue, para similaridade semântica em português/inglês).
    * **Banco de Dados Vetorial:** FAISS (Facebook AI Similarity Search) para indexação e recuperação de vetores de baixa latência.
* **Modelo de Linguagem Grande (LLM):** OpenAI GPT-4o (Geração de respostas precisas, contextualizadas e amigáveis, guiadas por engenharia de prompt).
* **Interface:** Streamlit (aplicação web interativa).
* **Capacidade Multilíngue:** Suporta perguntas em português, com base em documentação em inglês, e responde no idioma da consulta.

### Configuração e Execução Local

1.  **Clone o Repositório:**
    ```bash
    git clone [https://github.com/SEU_USUARIO_GITHUB/databricks-rag-study-assistant.git](https://github.com/SEU_USUARIO_GITHUB/databricks-rag-study-assistant.git)
    cd databricks-rag-study-assistant
    ```
2.  **Crie e Ative o Ambiente Virtual:**
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```
3.  **Instale as Dependências:**
    ```bash
    pip install -r requirements.txt
    ```
4.  4.  **Baixe a Documentação PDF do Databricks:**
    Baixe o arquivo `azure-databricks.pdf` (a documentação oficial de 17.800 páginas) no link abaixo e coloque-o no diretório `data/` deste projeto.
    [**Download da Documentação Oficial do Azure Databricks em PDF (540MB)**](https://drive.google.com/file/d/1AhsUstnfmnvA9vBkPvE5S9GO06gxXa-N/view?usp=sharing)
    *Observação: Este arquivo é muito grande para ser hospedado diretamente no GitHub, por isso o link externo.*
    Você também pode baixar a documentação mais recente do Azure Databricks diretamente no site oficial. Basta acessar o link [**AQUI**](https://learn.microsoft.com/en-us/azure/databricks/), ir até o final da página, no canto inferior esquerdo e clicar em BAIXAR PDF. Certifique de salva-lo como "azure-databricks.pdf" 
5.  **Prepare o Banco de Dados Vetorial (PDF):**
    Este script processa o PDF e cria o banco de dados vetorial FAISS inicial.
    ```bash
    python prepare_data.py
    ```
6.  **Faça o Web Scraping dos Artigos da Knowledge Base do Databricks:**
    Este script faz o scraping dos artigos da KB do Databricks e os salva como JSONs.
    ```bash
    python scrape_kb.py
    ```
7.  **Atualize o Banco de Dados Vetorial com os Artigos da KB:**
    Este script integra os artigos raspados ao seu banco de dados vetorial FAISS existente.
    ```bash
    python update_vector_db_with_kb.py
    ```
8.  **Defina a Chave da API da OpenAI:**
    Obtenha sua Chave da API da OpenAI em [platform.openai.com](https://platform.openai.com/api-keys) e defina-a como uma variável de ambiente na sua sessão do terminal:
    ```bash
    # Windows (PowerShell)
    $env:OPENAI_API_KEY="SUA_CHAVE_API"
    # macOS/Linux
    export OPENAI_API_KEY="SUA_CHAVE_API"
    ```
9.  **Execute o Aplicativo Streamlit:**
    ```bash
    streamlit run app.py
    ```
