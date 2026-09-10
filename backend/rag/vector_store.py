"""Vector Store implementation using TF-IDF and Cosine Similarity."""

from typing import List, Dict, Any, Optional, Tuple
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class VectorStore:
    """In-memory vector database with TF-IDF embeddings and cosine similarity retrieval."""

    def __init__(self):
        self.documents: List[Dict[str, Any]] = []
        self.vectorizer: Optional[TfidfVectorizer] = None
        self.doc_vectors: Optional[np.ndarray] = None

    def add_documents(self, docs: List[Dict[str, Any]]) -> None:
        """Adds a list of documents and re-indexes the vector space."""
        for doc in docs:
            # Avoid duplicate IDs
            self.documents = [d for d in self.documents if d["id"] != doc["id"]]
            self.documents.append(doc)
        self._build_index()

    def add_document(self, doc: Dict[str, Any]) -> None:
        """Adds a single document and updates index."""
        self.add_documents([doc])

    def _build_index(self) -> None:
        """Builds TF-IDF vector matrix over all documents."""
        if not self.documents:
            self.vectorizer = None
            self.doc_vectors = None
            return

        corpus = []
        for doc in self.documents:
            # Combine title, category, and content for rich text representation
            combined_text = f"{doc.get('title', '')} {doc.get('category', '')} {doc.get('content', '')}"
            corpus.append(combined_text)

        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            stop_words='english',
            ngram_range=(1, 2),
            sublinear_tf=True
        )
        self.doc_vectors = self.vectorizer.fit_transform(corpus)

    def search(
        self,
        query: str,
        top_k: int = 4,
        category_filter: Optional[str] = None
    ) -> List[Tuple[Dict[str, Any], float]]:
        """
        Searches the vector store for documents matching the query.
        Returns list of (document, similarity_score) tuples sorted by score descending.
        """
        if not self.documents or self.vectorizer is None or self.doc_vectors is None:
            return []

        query_vec = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vec, self.doc_vectors)[0]

        results = []
        for idx, score in enumerate(similarities):
            doc = self.documents[idx]
            if category_filter and doc.get("category") != category_filter:
                continue
            results.append((doc, float(score)))

        # Sort descending by score
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
        self.vectorizer = None
        self.doc_vectors = None
