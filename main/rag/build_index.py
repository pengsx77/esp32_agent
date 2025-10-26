from sentence_transformers import SentenceTransformer
import faiss, json, numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

texts = json.load(open('main/rag/rag_data/knowledge_texts.json', 'r', encoding='utf-8'))
embs = model.encode(texts)
index = faiss.IndexFlatL2(embs.shape[1])
index.add(np.array(embs).astype('float32'))
faiss.write_index(index, 'main/rag/rag_data/knowledge_index.faiss')
print(f"✅ Knowledge index built with {len(texts)} documents.")
