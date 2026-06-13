
from document_processor import extract_text , create_chunks
from embedding_generator import create_embeddings
from database import build_faiss_index, save_index

text = extract_text("sample.pdf")
chunks=create_chunks(text)

embeddings = create_embeddings(chunks)

index = build_faiss_index(embeddings)

save_index(index)

print("FAISS index created successfully!")
#print(type(embeddings))
#print(embeddings.shape)