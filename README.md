# Resume AI Assistant

A professional **Retrieval-Augmented Generation (RAG) application** that allows users to upload a resume and ask natural-language questions about skills, experience, projects, education, and other resume content.

The application extracts resume content, creates semantic chunks, generates Gemini embeddings, stores them in a FAISS vector database, retrieves the most relevant content for each query, and generates grounded answers using Google Gemini.

## 🚀 Live Demo

**Streamlit App:**  
https://resume-rag-assistant-8csz4dzh t7y8dappvkgjy9i.streamlit.app

**GitHub Repository:**  
https://github.com/Mainuddin123/Resume-RAG-Assistant

## ✨ Features

- Upload resumes in **PDF, DOCX, TXT, and Markdown** formats
- Automatic document extraction and preprocessing
- Recursive document chunking with overlap
- Gemini-based text embeddings
- FAISS vector similarity search
- Query preprocessing
- Retrieval-Augmented Generation using Gemini
- Grounded answers based only on retrieved resume context
- Retrieved source display with page information
- Protection against unsupported or hallucinated answers
- Automatic re-indexing when a different resume is uploaded
- Chat history within the active session
- Clear chat and upload a new resume
- Retry and fallback handling for temporary Gemini API failures
- Professional dark-themed Streamlit interface
- Deployed on Streamlit Community Cloud

## 🏗️ Architecture

```text
                    ┌──────────────────────┐
                    │     Resume Upload    │
                    │   PDF/DOCX/TXT/MD   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Document Extraction  │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Text Cleaning        │
                    │ + Recursive Chunking │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Gemini Embeddings    │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ FAISS Vector Store   │
                    └──────────┬───────────┘
                               │
                               │
User Question ───────► Query Preprocessing
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Similarity Retrieval │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Context Construction │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Gemini LLM           │
                    │ Grounded Generation  │
                    └──────────┬───────────┘
                               │
                               ▼
                    Answer + Retrieved Sources
# RAG Pipeline

Upload
  ↓
Extract
  ↓
Clean
  ↓
Chunk
  ↓
Embed
  ↓
Index in FAISS
  ↓
Preprocess Query
  ↓
Retrieve Relevant Chunks
  ↓
Build Context
  ↓
Prompt Gemini
  ↓
Generate Grounded Answer

# 🛠️ Technology Stack

Component	Technology
Frontend	Streamlit
Programming Language	Python
RAG Framework	LangChain
LLM	Google Gemini
Embeddings	Gemini Embeddings
Vector Database	FAISS
PDF Processing	PyPDF
DOCX Processing	docx2txt
Environment Management	python-dotenv
Deployment	Streamlit Community Cloud
Version Control	Git / GitHub

# 📁 Project Structure

Resume-RAG-Assistant/
│
├── app.py
├── rag.py
├── build_index.py
├── requirements.txt
├── .gitignore
├── README.md
│
├── data/
│
└── vectorstore/

# app.py

Responsible for:

Streamlit interface
Resume upload
Session state
Chat interface
Resume processing orchestration
Displaying retrieved sources
User interaction

# build_index.py

Responsible for:

Document loading
Text cleaning
Chunking
Gemini embedding generation
FAISS index creation
Persisting the vector store

# rag.py

Responsible for:

Query preprocessing
Loading FAISS
Similarity retrieval
Context construction
RAG prompt generation
Gemini response generation
Retry/fallback handling
Returning answers and retrieved documents

# 🧩 Chunking Strategy

The project uses RecursiveCharacterTextSplitter with:
chunk_size    = 700
chunk_overlap = 120
> The goal is to balance retrieval precision with enough context for the LLM to generate useful answers.

# 🔎 Retrieval

For every user question:

The query is normalized.
FAISS performs similarity search.
The top relevant chunks are retrieved.
The chunks are combined into the RAG context.
Gemini receives the context together with the user question.
The model is instructed to answer only from the supplied resume context.

# 🛡️ Grounding

The application explicitly instructs the model not to invent resume information.

When the retrieved context does not contain the requested information, the assistant returns:

I couldn't find that information in the resume.

This helps reduce unsupported answers and keeps responses grounded in the uploaded document.

# ⚡ Reliability

Temporary Gemini service errors such as 503 UNAVAILABLE or rate/resource errors are handled with:

Retries
Exponential backoff
Fallback Gemini models

This prevents temporary model availability issues from immediately breaking the user interaction.

# 💬 Example Questions:

What are the candidate's technical skills?

Summarize the professional experience.

What projects has the candidate worked on?

What machine learning technologies are mentioned?

What Generative AI experience does the candidate have?

What is the candidate's educational background?

Does the resume mention FastAPI?

## 💻 Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/Mainuddin123/Resume-RAG-Assistant.git
cd Resume-RAG-Assistant

2. Create and activate a virtual environment

Windows:
python -m venv venv
venv\Scripts\activate

3. Install dependencies
pip install -r requirements.txt

4. Configure the Gemini API

Create a .env file in the project root:
GOOGLE_API_KEY=YOUR_GEMINI_API_KEY
> Replace YOUR_GEMINI_API_KEY with your actual Google Gemini API key.
Do not commit .env to GitHub.

5. Run the application
> python -m streamlit run app.py---> The application will open in your browser.

☁️ Deployment:

The application is deployed using Streamlit Community Cloud.
Repository: Mainuddin123/Resume-RAG-Assistant
Branch: main
Entry point: app.py
> The Gemini API key is configured securely through Streamlit Secrets.

# ✅ Validation:

The application was tested with:

Multiple resume uploads
Resume replacement
Technical skills queries
Project queries
Education queries
FAISS retrieval
Retrieved source display
Unsupported-information queries
Gemini temporary availability failures
Clear Chat
New Resume

A second resume was successfully uploaded and re-indexed with a different chunk count, confirming that the application can process a new resume at runtime.

# 🚀 Production Considerations:

The current implementation is well suited for a portfolio/demo deployment.

For a larger multi-user production system, future improvements would include:

Per-user or per-session vector stores
Persistent cloud storage
Authentication and authorization
Upload size and file-type validation
Better document parsing and OCR
Retrieval evaluation
RAG evaluation metrics
Observability and logging
Rate limiting
Background document processing
Database-backed metadata management

# 🔮 Future Improvements:

Hybrid search using keyword + vector retrieval
Re-ranking retrieved chunks
Query rewriting
Metadata filtering
Multi-resume comparison
Resume-to-job-description matching
ATS-style resume analysis
Resume scoring
Conversational memory
Evaluation dashboard
Cloud vector databases such as Pinecone, Qdrant, or pgvector

👨‍💻 Author
Khaja Mainuddin SK

AI/ML Engineer Aspirant focused on:

Machine Learning
Deep Learning
Generative AI
RAG
AI Agents
FastAPI
AI Automation

📄 License
This project is intended for educational, portfolio, and demonstration purposes.





