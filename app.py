 

from document_processor import extract_text , create_chunks
from embedding_generator import create_embeddings
from database import build_faiss_index, save_index
from retriever import retrieve
from medical_chatbot import generate_answer

text = extract_text("sample.pdf")
chunks=create_chunks(text)

embeddings = create_embeddings(chunks)

index = build_faiss_index(embeddings)

save_index(index)

print("FAISS index created successfully!")
#print(type(embeddings))
#print(embeddings.shape)

from flask import Flask,request,render_template
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/uploads",methods=["POST"])
@app.route("/upload", methods=["POST"])
def upload():

    global chunks

    if "file" not in request.files:
        return {"error": "No file uploaded"}

    file = request.files["file"]

    path = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    file.save(path)

    text = extract_text(path)

    chunks = create_chunks(text)

    embeddings = create_embeddings(chunks)

    index = build_faiss_index(
        embeddings
    )

    save_index(index)
    print("Total Chunks:",
      len(chunks))

    return {
        "message":
        "Document processed successfully"
    }
@app.route("/chat",methods=["POST"])

def chat():

    question=request.json["question"]

    context=retrieve(
        question,
        chunks
    )
    print ("Question:",question)
    print ("Context:",context)
    answer=generate_answer(
        question,
        "\n".join(context)
    )
    print("\n")
    print("="*50)
    print("QUESTION:", question)
    print("="*50)

    print("\nCONTEXT:\n")

    for item in context:
        print(item[:200])

    print("="*50)   
    return {
        "answer":answer
    }

if __name__=="__main__":
    app.run(debug=True)