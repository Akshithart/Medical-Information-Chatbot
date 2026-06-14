import faiss
from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

def retrieve(query, chunks):

    index = faiss.read_index(
        "vectorstore/faiss.index"
    )

    query_vector = model.encode([query])

    D, I = index.search(
        query_vector,
        3
    )

    result = []

    for idx in I[0]:

        if idx < len(chunks):

            result.append(
                chunks[idx]
            )

    return result