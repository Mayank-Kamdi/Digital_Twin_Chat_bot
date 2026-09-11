"""Vector Store implementation using pure Python TF-IDF and Cosine Similarity."""

from typing import List, Dict, Any, Optional, Tuple
import math
import re
from collections import Counter


class VectorStore:
    """In-memory vector database with pure Python TF-IDF embeddings and cosine similarity."""

    def __init__(self):
        self.documents: List[Dict[str, Any]] = []
        self.doc_vectors: List[Dict[str, float]] = []
        self.idf: Dict[str, float] = {}
        self.vocab: set = set()

    def add_documents(self, docs: List[Dict[str, Any]]) -> None:
        """Adds a list of documents and re-indexes the vector space."""
        for doc in docs:
            self.documents = [d for d in self.documents if d["id"] != doc["id"]]
            self.documents.append(doc)
        self._build_index()

    def add_document(self, doc: Dict[str, Any]) -> None:
        self.add_documents([doc])

    def _tokenize(self, text: str) -> List[str]:
        return re.findall(r'\b[a-z0-9]+\b', text.lower())

    def _build_index(self) -> None:
        if not self.documents:
            self.doc_vectors = []
            self.idf = {}
            self.vocab = set()
            return

        corpus_tokens = []
        doc_frequencies = Counter()

        for doc in self.documents:
            combined_text = f"{doc.get('title', '')} {doc.get('category', '')} {doc.get('content', '')}"
            tokens = self._tokenize(combined_text)
            corpus_tokens.append(tokens)
            for token in set(tokens):
                doc_frequencies[token] += 1
            self.vocab.update(tokens)

        num_docs = len(self.documents)
        self.idf = {token: math.log(num_docs / (1 + df)) + 1.0 for token, df in doc_frequencies.items()}

        self.doc_vectors = []
        for tokens in corpus_tokens:
            tf = Counter(tokens)
            vec = {}
            norm_sq = 0.0
            for token, count in tf.items():
                weight = count * self.idf.get(token, 1.0)
                vec[token] = weight
                norm_sq += weight * weight
            
            norm = math.sqrt(norm_sq) if norm_sq > 0 else 1.0
            # Normalize vector
            for token in vec:
                vec[token] /= norm
            self.doc_vectors.append(vec)

    def search(
        self,
        query: str,
        top_k: int = 4,
        category_filter: Optional[str] = None
    ) -> List[Tuple[Dict[str, Any], float]]:
        if not self.documents or not self.doc_vectors:
            return []

        query_tokens = self._tokenize(query)
        tf = Counter(query_tokens)
        query_vec = {}
        norm_sq = 0.0
        
        for token, count in tf.items():
            if token in self.vocab:
                weight = count * self.idf.get(token, 1.0)
                query_vec[token] = weight
                norm_sq += weight * weight
                
        query_norm = math.sqrt(norm_sq) if norm_sq > 0 else 1.0

        results = []
        for idx, doc_vec in enumerate(self.doc_vectors):
            doc = self.documents[idx]
            if category_filter and doc.get("category") != category_filter:
                continue
                
            score = 0.0
            if query_norm > 0:
                for token, weight in query_vec.items():
                    if token in doc_vec:
                        score += (weight / query_norm) * doc_vec[token]
            
            results.append((doc, float(score)))

        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]

    def get_document_by_id(self, doc_id: str) -> Optional[Dict[str, Any]]:
        for doc in self.documents:
            if doc["id"] == doc_id:
                return doc
        return None

    def get_all_documents(self) -> List[Dict[str, Any]]:
        return list(self.documents)

    def clear(self) -> None:
        self.documents.clear()
        self.doc_vectors.clear()
        self.idf.clear()
        self.vocab.clear()
