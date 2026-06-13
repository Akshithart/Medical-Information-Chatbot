 
from flask import Flask,request,render_template
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload",methods=["POST"])
def upload():

    file = request.files["file"]

    if file:
        path=os.path.join(UPLOAD_FOLDER,file.filename)
        file.save(path)

        return {
            "message":"Uploaded Successfully",
            "path":path
        }

    return {"error":"No file"}

if __name__=="__main__":
    app.run(debug=True)