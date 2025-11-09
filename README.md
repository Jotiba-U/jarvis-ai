🤖 Jarvis AI — Intelligent Document Assistant

Developed by: Jotiba Ugale
Powered by: Mistral · Ollama · Pinecone

📝 Overview

Jarvis AI is a hybrid web-based intelligent assistant that allows users to upload PDF documents and interact with them using natural language.
It can summarize, analyze, and explain the uploaded document in a concise, human-like manner — powered by the Mistral LLM running locally through Ollama.

This project demonstrates:
Modern Flask backend integration
Efficient LLM orchestration
Fast and accurate document parsing
Persistent vector-based memory (Pinecone)
A clean, responsive, and minimal chat interface

⚙️ Features
✅ Upload any PDF document (up to 10 MB)
✅ Summarize or explain multiple program files instantly
✅ Contextual memory using Pinecone
✅ Clean, professional chat interface
✅ Markdown-formatted AI responses
✅ Runs fully offline (via Ollama + Mistral)
✅ Built with Python · Flask · HTML · CSS · JS

🧩 Project Structure
Flask (Backend)
│
├── app/
│   ├── main.py            → Flask routes & core logic
│   ├── ollama_client.py   → Mistral model API (Ollama)
│   ├── memory.py          → Pinecone vector memory
│   └── file_utils.py      → PDF text extraction
│
├── templates/
│   └── chat.html          → Chat UI
│
├── static/
│   └── style.css          → UI Styling
│
├── uploads/               → Uploaded PDF storage
├── requirements.txt
├── .env                   → Pinecone & environment keys
└── README.md

🚀 Getting Started
1️⃣ Prerequisites
Ensure you have:
Python 3.10+
Ollama installed and serving locally → Download Ollama
Mistral model pulled:
ollama pull mistral

2️⃣ Clone the project
git clone https://github.com/yourusername/jarvis-ai.git
cd jarvis-ai

3️⃣ Set up your environment
python -m venv venv
venv\Scripts\activate    # (Windows)

Install dependencies:
pip install -r requirements.txt

4️⃣ Configure environment variables
env file in your root folder:
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_INDEX=jarvis-memory

5️⃣ Run Ollama server
ollama serve

6️⃣ Launch Flask app
python -m app.main

Then open your browser and visit →
👉 http://127.0.0.1:5000

💡 Usage
Click 📎 Upload and select your PDF
Wait for the “✅ File uploaded successfully” message
Ask questions like:
“Summarize this document”
“Explain each Python program”
“Analyze the code structure”
Jarvis replies in clean Markdown with bullet points and sections.

🖥️ Tech Stack
| Layer               | Technology                                        |
| :------------------ | :------------------------------------------------ |
| **Frontend**        | HTML5, CSS3, JavaScript *(DOMPurify + Marked.js)* |
| **Backend**         | Flask (Python)                                    |
| **LLM Engine**      | Mistral via Ollama                                |
| **Vector DB**       | Pinecone                                          |
| **Embedding Model** | Sentence-Transformers (MiniLM-L6-v2)              |
| **PDF Parser**      | PyMuPDF (fitz)                                    |


📦 Dependencies
Flask==3.0.0
python-dotenv==1.0.1
pinecone==4.0.0
PyMuPDF==1.24.1
requests==2.31.0
sentence-transformers==2.2.2

Install all dependencies:
pip install -r requirements.txt

🧠 Example Interaction
You:
Summarize the uploaded document.
Jarvis:
✅ The uploaded PDF contains six Python programs focusing on:
Matrix operations (addition, multiplication, transpose)
Dictionary creation and manipulation
Set operations and basic iteration
Each program uses user input and follows a procedural coding style.


🧾 Credits
Developed with ❤️ by Jotiba Ugale