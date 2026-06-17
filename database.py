import sqlite3

import faiss
import numpy as np


def build_faiss_index(
        embeddings):

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(
        dimension
    )

    index.add(
        np.array(embeddings)
    )

    return index


def save_index(index):
    

    index = faiss.read_index(
    "vectorstore/faiss.index"
)

    print(
    "Total vectors:",
    index.ntotal
)
    print ("Dimension:",index.d)
    faiss.write_index(
        index,
        "vectorstore/faiss.index"
    )

DB_NAME = "medical_chatbot.db"

def create_tables():

    conn = sqlite3.connect(
        DB_NAME
    )

    cursor = conn.cursor()

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS chat_history (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        question TEXT,

        context TEXT,

        answer TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )

    """)

    conn.commit()

    conn.close()

def save_chat(

    question,

    context,

    answer

):

    conn = sqlite3.connect(
        DB_NAME
    )

    cursor = conn.cursor()

    cursor.execute(

    """

    INSERT INTO chat_history

    (
        question,
        context,
        answer
    )

    VALUES

    (
        ?,
        ?,
        ?
    )

    """,

    (
        question,
        context,
        answer
    )

    )

    conn.commit()

    conn.close()

def get_history():

    conn = sqlite3.connect(
        DB_NAME
    )

    cursor = conn.cursor()

    cursor.execute("""

    SELECT *

    FROM chat_history

    ORDER BY id DESC

    """)

    data = cursor.fetchall()

    conn.close()

    return data

def get_connection():

    conn = sqlite3.connect(
        DB_NAME
    )

    conn.row_factory = sqlite3.Row

    return conn