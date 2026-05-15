import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class TFIDFSimilarityEngine:
    @staticmethod
    def calculate_similarity(text_a: str, text_b: str) -> float:
        """
        Calculates mathematical geometric similarity score based on standard linear vector space formulations.
        """
        if not text_a.strip() or not text_b.strip():
            return 0.0
        
        try:
            vectorizer = TfidfVectorizer()
            tfidf_matrix = vectorizer.fit_transform([text_a, text_b])
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
            return float(similarity[0][0])
        except Exception:
            return 0.0