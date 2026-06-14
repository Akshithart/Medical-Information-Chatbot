
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)
index = faiss.read_index(
        "vectorstore/faiss.index"
    )


def retrieve(
        query,
        chunks):

    

    query_embedding = model.encode(
        [query]
    )
    query_embedding=np.array(query_embedding).astype("float32")

    D, I = index.search(
        query_embedding,
        3
    )

    results = []

    for idx in I[0]:

        if idx < len(chunks) and idx!=-1:

            results.append(
                chunks[idx]
            )

    return results