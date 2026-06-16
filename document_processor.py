import pdfplumber
import os


def extract_text(file_path):

    extension = os.path.splitext(
        file_path
    )[1].lower()

    # PDF
    if extension == ".pdf":

        text = ""

        with pdfplumber.open(
            file_path
        ) as pdf:

            for page in pdf.pages:

                page_text = page.extract_text()

                if page_text:

                    text += (
                        page_text +
                        "\n"
                    )

        return text

    # TXT
    elif extension == ".txt":

        with open(
            file_path,
            "r",
            encoding="utf-8",
            errors="ignore"
        ) as file:

            return file.read()

    return ""


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