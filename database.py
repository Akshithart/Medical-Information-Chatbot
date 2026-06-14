 
import faiss
import numpy as np

def build_faiss_index(embeddings):

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(
        dimension
    )

    index.add(
        np.array(embeddings)
    )
    faiss.write_index(
        index,
        "vectorstore/faiss.index"
    )

    return index

def save_index(index):
    faiss.write_index(
        index,
        "vectorstore/faiss.index"
    )

import sqlite3

conn=sqlite3.connect(
"database/medical.db"
)

cursor=conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS
chat_history(
id INTEGER PRIMARY KEY,
question TEXT,
answer TEXT
)
""")

conn.commit()