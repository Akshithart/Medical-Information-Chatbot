
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from nlp_processor import preprocess_query

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)
index = faiss.read_index(
        "vectorstore/faiss.index"
    )


def retrieve(
        query,
        chunks):

    query = preprocess_query(
    query
)

    query_embedding = model.encode(
    [query]
)
    D, I = index.search(
        query_embedding,
        2
    )
    print(
    "Distances:",
    D
)

    print(
    "Indexes:",
    I
)
    results = []

    for idx in I[0]:

        if idx < len(chunks) and idx!=-1:

            results.append(
                chunks[idx]
            )

    return results