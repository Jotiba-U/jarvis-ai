"""
Jarvis AI – Intelligent Document Assistant
Developed by: Jotiba Ugale
Model: Mistral (via Ollama)
Description:
    A Flask-based web application that allows users to upload PDF documents
    and interact with them using AI. Jarvis can summarize, analyze, and explain
    document contents using the Mistral LLM.
"""

from flask import Flask, render_template, request, jsonify
import os
import random
import re

# Local imports
from app.file_utils import extract_text_from_pdf
from app.ollama_client import OllamaLLM
from app.memory import store_memory, retrieve_memory

# =====================================================
# 🌐 APP INITIALIZATION
# =====================================================
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"

# Initialize Ollama client with Mistral model
llm = OllamaLLM(model="mistral")

# In-memory user data storage
user_docs = {}

# =====================================================
# ⚙️ SYSTEM PROMPT (Personality + Behavior)
# =====================================================
SYSTEM_PROMPT = (
    "You are Jarvis AI, a professional, precise, and concise assistant developed by Jotiba Ugale. "
    "You specialize in summarizing, explaining, and analyzing technical documents. "
    "All responses must be cleanly formatted in Markdown, factual, and human-readable. "
    "Avoid unnecessary repetition or vague language. Focus only on the document’s content."
)

# Keywords for detection
GREETINGS = ["hi", "hello", "hey", "good morning", "good evening"]
DOC_WORDS = ["summarize", "summary", "explain", "analyze", "document", "file", "content", "details", "program", "pdf"]

# =====================================================
# 🧹 TEXT PREPROCESSOR
# =====================================================
def clean_text(text: str) -> str:
    """
    Cleans raw PDF text for model processing.
    Reduces whitespace and limits token size for optimal speed.
    """
    text = re.sub(r"\s+", " ", text).strip()
    return text[:7000]  # ~8K tokens is Mistral’s sweet spot


# =====================================================
# 🏠 HOME ROUTE
# =====================================================
@app.route("/")
def index():
    """Renders the main chat interface."""
    return render_template("chat.html")


# =====================================================
# 📁 FILE UPLOAD ROUTE
# =====================================================
@app.route("/upload", methods=["POST"])
def upload_file():
    """Handles PDF upload and text extraction."""
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    save_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(save_path)

    # Extract PDF text
    text = extract_text_from_pdf(save_path)
    if not text:
        return jsonify({"error": "No readable text found in the file."}), 400

    # Store user data in memory and Pinecone
    user_docs["jotiba"] = text
    store_memory("jotiba", "document_upload", text[:1000])

    return jsonify({"message": f"✅ File '{file.filename}' uploaded successfully!"})


# =====================================================
# 💬 CHAT / SUMMARIZATION ROUTE
# =====================================================
@app.route("/chat", methods=["POST"])
def chat():
    """Processes user messages and generates AI responses."""
    data = request.get_json()
    user_message = (data.get("message") or "").strip()
    user_id = data.get("user_id", "jotiba")

    if not user_message:
        return jsonify({"response": "Please type something to begin."})

    msg_lower = user_message.lower()

    # 1️⃣ Handle greetings instantly
    if any(word in msg_lower for word in GREETINGS) and len(user_message.split()) <= 3:
        reply = random.choice([
            "Hey 👋, I'm Jarvis — your AI assistant. Upload a PDF, and I’ll summarize or explain it!",
            "Hello! I'm Jarvis, here to help you analyze your document.",
            "Hi there! Upload a file anytime, and I’ll extract and summarize its contents."
        ])
        store_memory(user_id, user_message, reply)
        return jsonify({"response": reply})

    # 2️⃣ Retrieve context
    doc_ctx = user_docs.get(user_id, "")
    memory_ctx = retrieve_memory(user_id, user_message)

    # 3️⃣ Determine if the user wants document analysis
    wants_doc = any(word in msg_lower for word in DOC_WORDS)
    if wants_doc and doc_ctx:
        cleaned_text = clean_text(doc_ctx)
        prompt = f"""
{SYSTEM_PROMPT}

Summarize and analyze the entire document provided below.
If it contains multiple programs or sections, list each with a short explanation.
Format the output clearly in Markdown.

<Document>
{cleaned_text}
</Document>

Jarvis:
"""
    else:
        context = memory_ctx or ""
        prompt = f"""
{SYSTEM_PROMPT}

Use past context if relevant; otherwise, respond conversationally.

Context: {context}
User: {user_message}
Jarvis:
"""

    # 4️⃣ Generate AI Response
    try:
        response = llm.chat(prompt).strip()
    except Exception as e:
        print(f"[Error] LLM failure: {e}")
        response = "⚠️ Sorry, something went wrong while generating the response."

    # 5️⃣ Save to memory
    store_memory(user_id, user_message, response)

    return jsonify({"response": response})


# =====================================================
# 🚀 APP ENTRY POINT
# =====================================================
if __name__ == "__main__":
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    print("🚀 Jarvis AI running at http://127.0.0.1:5000 (Model: Mistral)")
    app.run(debug=True)
