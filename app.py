from flask import Flask, request, render_template, jsonify
import os

from document_processor import extract_text, create_chunks
from embedding_generator import create_embeddings
from database import build_faiss_index, save_index
from retriever import retrieve
from medical_chatbot import generate_answer
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from database import (
    create_tables,
    save_chat,
    get_history,get_connection
)

from reportlab.lib.styles import getSampleStyleSheet
create_tables()
app = Flask(__name__)

cache = {}
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

current_filename = "No file uploaded"
uploaded_files=[]
chunks = []


@app.route("/")
def home():
    return render_template("upload.html")


@app.route("/upload", methods=["POST"])
def upload():

    global chunks
    global uploaded_files
    global current_filename

    if "files" not in request.files:
        return jsonify({
            "error": "No files uploaded"
        }), 400

    files = request.files.getlist("files")

    if len(files) == 0:
        return jsonify({
            "error": "No files selected"
        }), 400

    all_chunks = []
    uploaded_files = []

    for file in files:

        if file.filename == "":
            continue

        filepath = os.path.join(
            UPLOAD_FOLDER,
            file.filename
        )

        file.save(filepath)

        uploaded_files.append(
            file.filename
        )

        text = extract_text(
            filepath
        )

        if len(text.strip()) == 0:
            continue

        file_chunks = create_chunks(
            text
        )

        all_chunks.extend(
            file_chunks
        )

    if len(all_chunks) == 0:
        return jsonify({
            "error": "No readable content found"
        }), 400

    chunks = all_chunks

    embeddings = create_embeddings(
        chunks
    )

    index = build_faiss_index(
        embeddings
    )

    save_index(index)
    import retriever

    retriever.index = index
    current_filename = ", ".join(
        uploaded_files
    )

    return jsonify({
        "message": "Documents processed successfully",
        "files": uploaded_files,
        "chunks": len(chunks)
    })

@app.route("/chat", methods=["POST"])
def chat():

    global chunks
    
    question = request.json.get(
        "question",
        ""
    ).strip()

    if not question:
        return jsonify({
            "error": "Question cannot be empty"
        }), 400
    
    
    # CACHE CHECK
    if question in cache:

        cached_response = cache[question]

        save_chat(
            question,
            cached_response["context"],
            cached_response["answer"]
        )

        return jsonify(
            cached_response
        )

    # DOCUMENT CHECK
    if not chunks:
        return jsonify({
            "answer":
            "Please upload a document first.",
            "context": ""
        })

    context = retrieve(
        question,
        chunks
    )

    if len(context) == 0:
        return jsonify({
            "answer":
            "Information not found in uploaded document.",
            "context": ""
        })

    context_text = "\n\n".join(
        context
    )

    try:

        answer = generate_answer(
            question,
            context_text
        )

        save_chat(
            question,
            context_text,
            answer
        )

        response_data = {
    "answer": answer,
    "context": context_text[:500] + "..."
}

        cache[question] = response_data

        return jsonify(
            response_data
        )

    except Exception as e:

        print("LLM ERROR:", e)

        return jsonify({
            "answer":
            f"Model Error: {str(e)}",
            "context":
            context_text
        })

@app.route("/chatpage")
def chatpage():

    pdf_uploaded = len(uploaded_files) > 0

    faiss_ready = len(chunks) > 0

    return render_template(
        "chat.html",
        filename=current_filename,
        files=uploaded_files,
        pdf_uploaded=pdf_uploaded,
        faiss_ready=faiss_ready
    )

@app.route("/download-report", methods=["POST"])
def download_report():

    data = request.json

    question = data["question"]
    context = data["context"]
    answer = data["answer"]

    pdf_path = "static/report.pdf"

    doc = SimpleDocTemplate(pdf_path)

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "Medical Information Chatbot Report",
            styles["Title"]
        )
    )

    content.append(
        Spacer(1, 20)
    )

    content.append(
        Paragraph(
            f"<b>Question:</b> {question}",
            styles["BodyText"]
        )
    )

    content.append(
        Spacer(1,10)
    )

    content.append(
        Paragraph(
            f"<b>Retrieved Context:</b><br/>{context}",
            styles["BodyText"]
        )
    )

    content.append(
        Spacer(1,10)
    )

    content.append(
        Paragraph(
            f"<b>Generated Answer:</b><br/>{answer}",
            styles["BodyText"]
        )
    )

    doc.build(content)

    return jsonify({
        "pdf": "/static/report.pdf"
    })

@app.route(
    "/history",
    methods=["GET"]
)
def history():

    rows = get_history()

    result = []

    for row in rows:

        result.append({

            "id": row[0],

            "question": row[1],

            "context": row[2],

            "answer": row[3],

            "created_at": row[4]

        })

    return jsonify(
        result
    )

@app.route(
    "/clear-history",
    methods=["POST"]
)
def clear_history():

    import sqlite3

    conn = sqlite3.connect(
        "medical_chatbot.db"
    )

    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM chat_history"
    )

    conn.commit()
    conn.close()

    return jsonify({
        "message":"History cleared"
    })

if __name__ == "__main__":
    app.run(debug=True)

