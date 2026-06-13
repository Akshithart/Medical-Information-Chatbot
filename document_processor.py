 
import pdfplumber

def extract_text(pdf_path):

    text=""

    with pdfplumber.open(pdf_path) as pdf:

        for page in pdf.pages:
            text += page.extract_text()
            

    return text

def create_chunks(text,
                  chunk_size=500):

    chunks=[]

    for i in range(
        0,
        len(text),
        chunk_size
    ):
        chunks.append(
            text[i:i+chunk_size]
        )

    return chunks