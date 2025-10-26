import os
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

DATA_DIR = os.path.join(os.path.dirname(__file__), "rag_data")
INDEX_PATH = os.path.join(DATA_DIR, "index.faiss")
TEXT_PATH = os.path.join(DATA_DIR, "knowledge_texts.json")

class RAGEngine:
    def __init__(self, model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"):
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.texts = []
        self._load_index()

    def _load_index(self):
        if not os.path.exists(TEXT_PATH):
            raise FileNotFoundError(f"Missing {TEXT_PATH}")
        with open(TEXT_PATH, "r", encoding="utf-8") as f:
            self.texts = json.load(f)
        if os.path.exists(INDEX_PATH):
            self.index = faiss.read_index(INDEX_PATH)
        else:
            self._build_index()

    def _build_index(self):
        embeddings = self.model.encode(self.texts, convert_to_numpy=True, show_progress_bar=True)
        index = faiss.IndexFlatL2(embeddings.shape[1])
        index.add(embeddings)
        faiss.write_index(index, INDEX_PATH)
        self.index = index

    def retrieve(self, query, top_k=3):
        if self.index is None:
            self._load_index()
        q_vec = self.model.encode([query], convert_to_numpy=True)
        D, I = self.index.search(q_vec, top_k)
        return [self.texts[i] for i in I[0]]
