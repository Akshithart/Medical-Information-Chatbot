 
import faiss
from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

index = faiss.read_index(
    "vectorstore/faiss.index"
)

def retrieve(query,chunks):

    query_vector=model.encode(
        [query]
    )

    D,I=index.search(
        query_vector,
        3
    )

    result=[]

    for idx in I[0]:
        result.append(
            chunks[idx]
        )

    return result