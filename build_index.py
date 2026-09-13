import os
import shutil

from langchain_core.documents import Document

from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    TextLoader,
)

from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_google_genai import GoogleGenerativeAIEmbeddings

from langchain_community.vectorstores import FAISS


# ============================================================
# CONFIGURATION
# ============================================================

VECTORSTORE_PATH = "vectorstore"


# ============================================================
# LOAD DOCUMENT
# ============================================================

def load_document(file_path: str):
    """
    Load a supported resume document.

    Supported formats:
    - PDF
    - DOCX
    - TXT
    - MD
    """

    extension = os.path.splitext(
        file_path
    )[1].lower()

    if extension == ".pdf":

        loader = PyPDFLoader(
            file_path
        )

    elif extension == ".docx":

        loader = Docx2txtLoader(
            file_path
        )

    elif extension in [".txt", ".md"]:

        loader = TextLoader(
            file_path,
            encoding="utf-8",
        )

    else:

        raise ValueError(
            "Unsupported file format. "
            "Supported formats: PDF, DOCX, TXT, MD."
        )

    documents = loader.load()

    if not documents:

        raise ValueError(
            "No readable content was found in the document."
        )

    return documents


# ============================================================
# CLEAN DOCUMENTS
# ============================================================

def clean_documents(documents):
    """
    Normalize extracted document text.
    """

    cleaned_documents = []

    for document in documents:

        text = document.page_content

        # Normalize spaces
        text = " ".join(
            text.split()
        )

        text = text.strip()

        if not text:
            continue

        cleaned_documents.append(
            Document(
                page_content=text,
                metadata=document.metadata.copy(),
            )
        )

    return cleaned_documents


# ============================================================
# CHUNK DOCUMENT
# ============================================================

def create_chunks(documents):
    """
    Split documents into overlapping chunks.
    """

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=120,
        length_function=len,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            "",
        ],
    )

    chunks = text_splitter.split_documents(
        documents
    )

    if not chunks:

        raise ValueError(
            "Unable to create document chunks."
        )

    return chunks


# ============================================================
# CREATE EMBEDDINGS
# ============================================================

def create_embeddings():

    return GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-2-preview"
    )


# ============================================================
# CREATE FAISS
# ============================================================

def create_vectorstore(chunks):

    embeddings = create_embeddings()

    vectorstore = FAISS.from_documents(
        chunks,
        embeddings,
    )

    return vectorstore


# ============================================================
# SAVE FAISS
# ============================================================

def save_vectorstore(vectorstore):

    if os.path.exists(
        VECTORSTORE_PATH
    ):

        shutil.rmtree(
            VECTORSTORE_PATH
        )

    os.makedirs(
        VECTORSTORE_PATH,
        exist_ok=True,
    )

    vectorstore.save_local(
        VECTORSTORE_PATH
    )


# ============================================================
# BUILD INDEX
# ============================================================

def build_index(file_path: str):
    """
    Complete ingestion pipeline.

    File
      ↓
    Extraction
      ↓
    Cleaning
      ↓
    Chunking
      ↓
    Embeddings
      ↓
    FAISS
      ↓
    Save
    """

    print("\nStarting document processing...")

    # --------------------------------------------------------
    # 1. Load
    # --------------------------------------------------------

    print("1. Loading document...")

    documents = load_document(
        file_path
    )

    print(
        f"   Loaded sections: {len(documents)}"
    )


    # --------------------------------------------------------
    # 2. Clean
    # --------------------------------------------------------

    print("2. Cleaning document...")

    documents = clean_documents(
        documents
    )

    if not documents:

        raise ValueError(
            "No usable text remained after cleaning."
        )


    # --------------------------------------------------------
    # 3. Chunk
    # --------------------------------------------------------

    print("3. Creating chunks...")

    chunks = create_chunks(
        documents
    )

    print(
        f"   Created chunks: {len(chunks)}"
    )


    # --------------------------------------------------------
    # 4. Embeddings + FAISS
    # --------------------------------------------------------

    print(
        "4. Creating embeddings and FAISS index..."
    )

    vectorstore = create_vectorstore(
        chunks
    )


    # --------------------------------------------------------
    # 5. Save
    # --------------------------------------------------------

    print("5. Saving vectorstore...")

    save_vectorstore(
        vectorstore
    )


    print(
        "\n✓ Vectorstore created successfully."
    )

    print(
        f"✓ Location: {VECTORSTORE_PATH}"
    )

    print(
        f"✓ Total chunks: {len(chunks)}"
    )


    return vectorstore, len(chunks)


# ============================================================
# COMMAND LINE
# ============================================================

if __name__ == "__main__":

    file_path = os.path.join(
        "data",
        "resume.pdf",
    )

    if not os.path.exists(
        file_path
    ):

        print(
            f"\nError: file not found:\n{file_path}"
        )

        print(
            "\nPlace the resume inside the "
            "'data' folder."
        )

    else:

        build_index(
            file_path
        )