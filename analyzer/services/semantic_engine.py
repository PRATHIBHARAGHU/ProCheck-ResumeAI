import logging
import numpy as np

logger = logging.getLogger(__name__)

class SemanticSimilarityEngine:
    def __init__(self):
        self.model = None
        try:
            from sentence_transformers import SentenceTransformer
            # Lightweight semantic transformer module optimized for micro-computing runtimes
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
        except Exception as e:
            logger.warning(f"Could not load SentenceTransformer automatically, running fallback vectorizer model setup: {e}")

    def calculate_semantic_score(self, text_a: str, text_b: str) -> float:
        """
        Extracts embeddings and determines advanced contextual alignment matching parameters.
        """
        if not text_a.strip() or not text_b.strip():
            return 0.0
            
        if self.model:
            try:
                embeddings = self.model.encode([text_a, text_b])
                vec_a = embeddings[0].reshape(1, -1)
                vec_b = embeddings[1].reshape(1, -1)
                from sklearn.metrics.pairwise import cosine_similarity
                return float(cosine_similarity(vec_a, vec_b)[0][0])
            except Exception as e:
                logger.error(f"Semantic model inference tracking fault: {e}")
        
        # Fallback pseudo-semantic token tracking intersection ratio model if dependencies fail to process
        tokens_a = set(text_a.lower().split())
        tokens_b = set(text_b.lower().split())
        if not tokens_a or not tokens_b:
            return 0.0
        intersection = tokens_a.intersection(tokens_b)
        union = tokens_a.union(tokens_b)
        return float(len(intersection) / len(union))