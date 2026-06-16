
import pdfplumber


def extract_text(pdf_path):

    text = ""

    with pdfplumber.open(pdf_path) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    return text


def create_chunks(
        text,
        chunk_size=1500):

    chunks = []

    for i in range(
            0,
            len(text),
            chunk_size):

        chunks.append(
            text[i:i+chunk_size]
        )

    return chunks