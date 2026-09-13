import hashlib
import os
import tempfile

import streamlit as st

from build_index import build_index
from rag import ask_rag


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Resume AI Assistant",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# PROFESSIONAL DARK THEME
# ============================================================

st.markdown(
    """
<style>

.stApp {
    background-color: #0b0f17;
    color: #e5e7eb;
}

[data-testid="stAppViewContainer"] {
    background-color: #0b0f17;
}

..block-container {
    max-width: 1180px;
    padding-top: 0.5rem;
    padding-bottom: 4rem;
}

/* Remove Streamlit top header */
[data-testid="stHeader"] {
    display: none;
}

header {
    display: none;
}

/* Remove remaining top spacing */
.block-container {
    padding-top: 0.8rem !important;
}

/* Sidebar */

[data-testid="stSidebar"] {
    background-color: #111722;
    border-right: 1px solid #263244;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #f8fafc !important;
}

[data-testid="stSidebar"] p {
    color: #94a3b8 !important;
}

/* Headings */

h1,
h2,
h3 {
    color: #f8fafc !important;
}

h1 {
    font-weight: 800 !important;
    letter-spacing: -1px;
}

/* File uploader */

[data-testid="stFileUploader"] {
    background-color: #151c29;
    border: 1px dashed #3b4d65;
    border-radius: 10px;
    padding: 0.5rem;
}

/* Buttons */

.stButton > button {
    background-color: #151c29;
    border: 1px solid #334155;
    color: #e2e8f0;
    border-radius: 8px;
    font-weight: 600;
}

.stButton > button:hover {
    border-color: #3b82f6;
    color: #60a5fa;
}

/* Chat */

[data-testid="stChatMessage"] {
    border-radius: 12px;
}

[data-testid="stChatMessageContent"] {
    color: #e2e8f0;
    line-height: 1.7;
}

/* Chat input */

[data-testid="stChatInput"] {
    border-color: #334155;
}

/* Expanders */

[data-testid="stExpander"] {
    background-color: #111722;
    border: 1px solid #263244;
    border-radius: 10px;
}

/* Metrics */

[data-testid="stMetric"] {
    background-color: #111722;
    border: 1px solid #263244;
    border-radius: 12px;
    padding: 12px;
}

[data-testid="stMetricLabel"] {
    color: #94a3b8 !important;
}

[data-testid="stMetricValue"] {
    color: #f8fafc !important;
}

/* Alerts */

[data-testid="stAlert"] {
    border-radius: 10px;
}

/* Divider */

hr {
    border-color: #263244 !important;
}

/* ==========================================================
   UPLOAD RESUME BOX
   ========================================================== */

[data-testid="stFileUploader"] {
    background-color: #111827 !important;
    border: 1px solid #334155 !important;
    border-radius: 12px !important;
    padding: 8px !important;
}

[data-testid="stFileUploaderDropzone"] {
    background-color: #151c29 !important;
    border: 1px dashed #475569 !important;
    border-radius: 10px !important;
}

[data-testid="stFileUploaderDropzone"] * {
    color: #cbd5e1 !important;
}

[data-testid="stFileUploaderDropzoneInstructions"] {
    color: #cbd5e1 !important;
}

[data-testid="stFileUploaderDropzoneInstructions"] small {
    color: #94a3b8 !important;
}

[data-testid="stFileUploaderDropzone"] button {
    background-color: #1e293b !important;
    color: #e2e8f0 !important;
    border: 1px solid #475569 !important;
    border-radius: 8px !important;
}

[data-testid="stFileUploaderDropzone"] button:hover {
    background-color: #2563eb !important;
    color: #ffffff !important;
    border-color: #3b82f6 !important;
}

[data-testid="stFileUploaderFile"] {
    background-color: #1a2333 !important;
    border: 1px solid #334155 !important;
    border-radius: 8px !important;
}

[data-testid="stFileUploaderFile"] * {
    color: #e2e8f0 !important;
}

[data-testid="stFileUploaderFile"] small {
    color: #94a3b8 !important;
}

[data-testid="stFileUploaderFile"] button {
    background: transparent !important;
    color: #cbd5e1 !important;
}

[data-testid="stFileUploaderFile"] button:hover {
    color: #f87171 !important;
}


/* ==========================================================
   CHAT TYPING BOX
   ========================================================== */

[data-testid="stChatInput"] {
    background-color: #ffffff !important;
    border: 1px solid #d1d5db !important;
    border-radius: 10px !important;
}

[data-testid="stChatInput"] textarea {
    background-color: #ffffff !important;
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #6b7280 !important;
    opacity: 1 !important;
}

[data-testid="stChatInput"] button {
    color: #374151 !important;
}

/* ==========================================================
   CHAT BOTTOM AREA
   ========================================================== */

[data-testid="stBottom"] {
    background: #0b0f17 !important;
    border-top: 1px solid #263244 !important;
}

[data-testid="stBottom"] > div {
    background: #0b0f17 !important;
}


/* ==========================================================
   WHITE CHAT INPUT
   ========================================================== */

[data-testid="stChatInput"] {
    background: #ffffff !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 10px !important;
}

[data-testid="stChatInput"] textarea {
    background: #ffffff !important;
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #64748b !important;
    opacity: 1 !important;
}

/* ==========================================================
   RAINBOW MAIN HEADING
   ========================================================== */

.rainbow-title {
    font-size: 3rem;
    font-weight: 850;
    letter-spacing: -1.5px;
    line-height: 1.15;

    background: linear-gradient(
        90deg,
        #ff4d4d,
        #ff9f43,
        #ffe66d,
        #4cd97b,
        #45aaf2,
        #7d5fff,
        #d56cff,
        #ff4d9d
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;

    margin-bottom: 0.5rem;
}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

if "resume_name" not in st.session_state:
    st.session_state.resume_name = None

if "chunk_count" not in st.session_state:
    st.session_state.chunk_count = 0

if "resume_hash" not in st.session_state:
    st.session_state.resume_hash = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# ============================================================
# HELPERS
# ============================================================

def calculate_file_hash(file_bytes: bytes) -> str:
    return hashlib.sha256(file_bytes).hexdigest()


def reset_chat():
    st.session_state.chat_history = []


def reset_resume():
    st.session_state.vectorstore = None
    st.session_state.resume_name = None
    st.session_state.chunk_count = 0
    st.session_state.resume_hash = None
    st.session_state.chat_history = []


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("📄 Resume AI")

    st.caption(
        "Intelligent resume analysis using "
        "Retrieval-Augmented Generation."
    )

    st.divider()

    st.subheader("Upload Resume")

    uploaded_file = st.file_uploader(
        "Choose a resume",
        type=[
            "pdf",
            "docx",
            "txt",
            "md",
        ],
        help="Supported formats: PDF, DOCX, TXT and Markdown.",
    )

    st.caption(
        "PDF • DOCX • TXT • Markdown"
    )

    # ========================================================
    # PROCESS UPLOADED RESUME
    # ========================================================

    if uploaded_file is not None:

        file_bytes = uploaded_file.getvalue()

        current_hash = calculate_file_hash(
            file_bytes
        )

        # Only rebuild index when the file changes
        if current_hash != st.session_state.resume_hash:

            temp_path = None

            try:

                extension = os.path.splitext(
                    uploaded_file.name
                )[1].lower()

                # Save uploaded file temporarily
                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=extension,
                ) as temp_file:

                    temp_file.write(
                        file_bytes
                    )

                    temp_path = temp_file.name

                # Build FAISS
                with st.spinner(
                    "Processing resume..."
                ):

                    vectorstore, chunk_count = build_index(
                        temp_path
                    )

                # Store active session information
                st.session_state.vectorstore = vectorstore

                st.session_state.resume_name = (
                    uploaded_file.name
                )

                st.session_state.chunk_count = (
                    chunk_count
                )

                st.session_state.resume_hash = (
                    current_hash
                )

                st.session_state.chat_history = []

                st.success(
                    "Resume processed successfully."
                )

                st.rerun()

            except Exception as error:

                st.error(
                    "Resume processing failed."
                )

                with st.expander(
                    "Technical details"
                ):
                    st.code(
                        str(error)
                    )

            finally:

                if (
                    temp_path is not None
                    and os.path.exists(temp_path)
                ):
                    os.remove(
                        temp_path
                    )

    st.divider()

    # ========================================================
    # CURRENT RESUME
    # ========================================================

    st.subheader("Current Resume")

    if st.session_state.vectorstore is not None:

        st.success(
            "RAG assistant ready"
        )

        st.write(
            f"📄 **{st.session_state.resume_name}**"
        )

        st.write(
            f"🧩 **{st.session_state.chunk_count}** "
            "document chunks"
        )

        st.write(
            "🔎 FAISS vector retrieval"
        )

        st.divider()

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "Clear Chat",
                use_container_width=True,
            ):

                reset_chat()
                st.rerun()

        with col2:

            if st.button(
                "New Resume",
                use_container_width=True,
            ):

                reset_resume()
                st.rerun()

    else:

        st.caption(
            "No resume uploaded yet."
        )

    st.divider()

    st.caption(
        "Embeddings • Chunking • FAISS • RAG • Gemini"
    )


# ============================================================
# MAIN HEADER
# ============================================================

st.markdown(
    """
    <h1 class="rainbow-title">
        📄 Resume AI Assistant
    </h1>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    "Upload a resume and ask natural-language questions "
    "about **skills, experience, projects, education and more.**"
)


# ============================================================
# EMPTY STATE
# ============================================================

if st.session_state.vectorstore is None:

    st.info(
        "👈 Upload a resume from the sidebar "
        "to start asking questions."
    )

    st.subheader(
        "What you can ask"
    )

    example_questions = [
        "What are the candidate's technical skills?",
        "Summarize the professional experience.",
        "What projects has the candidate worked on?",
        "What machine learning technologies are mentioned?",
        "What Generative AI experience does the candidate have?",
        "What is the candidate's educational background?",
        "Does the resume mention FastAPI?",
    ]

    for question in example_questions:
        st.markdown(
            f"- {question}"
        )

    st.stop()


# ============================================================
# RESUME METRICS
# ============================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Resume",
        st.session_state.resume_name,
    )

with col2:
    st.metric(
        "Document Chunks",
        st.session_state.chunk_count,
    )

with col3:
    st.metric(
        "Retrieval",
        "FAISS",
    )


# ============================================================
# CHAT HISTORY
# ============================================================

for message in st.session_state.chat_history:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )

        # Retrieved sources
        if (
            message["role"] == "assistant"
            and message.get("sources")
        ):

            with st.expander(
                "🔎 Retrieved Sources"
            ):

                for i, (
                    document,
                    score,
                ) in enumerate(
                    message["sources"],
                    start=1,
                ):

                    page = document.metadata.get(
                        "page"
                    )

                    if page is not None:
                        page_number = int(page) + 1
                    else:
                        page_number = "N/A"

                    st.markdown(
                        f"""
**Source {i}**

Page: `{page_number}`

Similarity score: `{score:.4f}`
"""
                    )

                    st.caption(
                        document.page_content
                    )

                    if i < len(
                        message["sources"]
                    ):
                        st.divider()


# ============================================================
# CHAT INPUT
# ============================================================

question = st.chat_input(
    "Ask something about this resume..."
)


# ============================================================
# PROCESS QUESTION
# ============================================================

if question:

    question = question.strip()

    if not question:

        st.warning(
            "Please enter a question."
        )

        st.stop()

    # --------------------------------------------------------
    # USER MESSAGE
    # --------------------------------------------------------

    st.session_state.chat_history.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.chat_message("user"):
        st.markdown(
            question
        )

    # --------------------------------------------------------
    # ASSISTANT
    # --------------------------------------------------------

    with st.chat_message("assistant"):

        try:

            with st.spinner(
                "Searching the resume..."
            ):

                # rag.py loads the saved FAISS
                # index from vectorstore/
                answer, results = ask_rag(
                    question,
                    vectorstore_path="vectorstore",
                    k=4,
                )

            st.markdown(
                answer
            )

            # ------------------------------------------------
            # SOURCES
            # ------------------------------------------------

            if results:

                with st.expander(
                    "🔎 Retrieved Sources"
                ):

                    for i, (
                        document,
                        score,
                    ) in enumerate(
                        results,
                        start=1,
                    ):

                        page = document.metadata.get(
                            "page"
                        )

                        if page is not None:
                            page_number = int(page) + 1
                        else:
                            page_number = "N/A"

                        st.markdown(
                            f"""
**Source {i}**

Page: `{page_number}`

Similarity score: `{score:.4f}`
"""
                        )

                        st.caption(
                            document.page_content
                        )

                        if i < len(results):
                            st.divider()

            # ------------------------------------------------
            # SAVE RESPONSE
            # ------------------------------------------------

            st.session_state.chat_history.append(
                {
                    "role": "assistant",
                    "content": answer,
                    "sources": results,
                }
            )

        except Exception as error:

            error_message = (
                "I couldn't generate an answer right now. "
                "Please try again."
            )

            st.error(
                error_message
            )

            with st.expander(
                "Technical details"
            ):
                st.code(
                    str(error)
                )