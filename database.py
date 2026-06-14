
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

    faiss.write_index(
        index,
        "vectorstore/faiss.index"
    )