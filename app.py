from flask import Flask, request, render_template, jsonify
import os

from document_processor import extract_text, create_chunks
from embedding_generator import create_embeddings
from database import build_faiss_index, save_index
from retriever import retrieve
from medical_chatbot import generate_answer,load_dotenv

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

chunks = []

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():

    global chunks

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"})

    file = request.files["file"]

    filepath = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    file.save(filepath)

    text = extract_text(filepath)

    chunks = create_chunks(text)

    embeddings = create_embeddings(chunks)

    index = build_faiss_index(embeddings)

    save_index(index)

    return jsonify({
        "message": "Document processed successfully",
        "chunks": len(chunks)
    })


'''@app.route("/chat", methods=["POST"])
def chat():

    global chunks

    data = request.get_json()

    question = data["question"]

    context = retrieve(
        question,
        chunks
    )

    answer = generate_answer(
        question,
        "\n".join(context)
    )
    print("\n===== RETRIEVED CONTEXT =====")
    print("\n".join(context))
    print("=============================\n")
    return jsonify({
        "answer": answer,
        "context": context
    
    })'''

@app.route("/chat", methods=["POST"])
def chat():

    question = request.json["question"]

    context = retrieve(
        question,
        chunks
    )

    answer = generate_answer(
        question,
        "\n".join(context)
    )

    return {
        "answer": answer
    }

if __name__ == "__main__":
    app.run(debug=True)