import pandas as pd
import faiss
import os
import numpy as np
from .embedding import get_embedding

# Paths relative to this file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(BASE_DIR, "data", "jewellery_metadata.csv")
INDEX_PATH = os.path.join(BASE_DIR, "data", "jewellery_faiss.index")

class SearchEngine:
    def __init__(self):
        print("Loading Database...")
        if not os.path.exists(INDEX_PATH):
            raise FileNotFoundError(f"Index file not found at {INDEX_PATH}! Did you run the Colab script?")
            
        self.df = pd.read_csv(CSV_PATH)
        self.index = faiss.read_index(INDEX_PATH)
        print(f"Database Loaded: {self.index.ntotal} Items")

    def search(self, query, top_k=5):
        query_vec = get_embedding(query).reshape(1, -1)
        
        # 1. Fetch more candidates for hybrid scoring (3x top_k)
        candidate_k = top_k * 3
        distances, indices = self.index.search(query_vec, candidate_k)
        
        candidates = []
        query_tokens = set(query.lower().split())
        
        for i, idx in enumerate(indices[0]):
            if idx >= 0 and idx < len(self.df):
                row = self.df.iloc[idx]
                dist = distances[0][i]
                
                # --- HYBRID SCORING LOGIC ---
                
                # 1. Vector Score (Normalize distance to 0-1 similarity)
                # Assuming L2 distance on normalized vectors: range approx 0.0 to 2.0
                # Using 1 / (1 + dist) as a simple similarity proxy
                vector_score = 1 / (1 + dist)
                
                # 2. Keyword Matching Score
                keyword_score = 0.0
                
                # Check Category (Generic Match - Reduced Weight)
                if str(row['category']).lower() in query_tokens:
                    keyword_score += 0.2
                
                # Check Caption (Specific Match - High Weight)
                # Split caption into words to check for keyword presence
                caption_words = str(row['caption']).lower().split()
                if any(w in query_tokens for w in caption_words):
                    keyword_score += 0.25
                    
                # Check Material (Medium Weight)
                material_words = str(row['material']).lower().split()
                if any(w in query_tokens for w in material_words):
                    keyword_score += 0.15
                    
                # Check Style (Low Weight)
                style_words = str(row['style']).lower().split()
                if any(w in query_tokens for w in style_words):
                    keyword_score += 0.1
                
                # 3. Final Hybrid Score
                # Combine Vector (Base) + Keywords (Boost)
                final_score = (vector_score * 0.7) + (keyword_score * 0.3)
                
                # Cap at 0.99 for display
                final_score = min(0.99, final_score)
                
                candidates.append({
                    "idx": idx,
                    "row": row,
                    "score": final_score
                })
        
        # 4. Sort by Hybrid Score (Descending)
        candidates.sort(key=lambda x: x['score'], reverse=True)
        
        # 5. Construct final results
        final_results = []
        for item in candidates[:top_k]:
            row = item['row']
            final_results.append({
                "image_name": str(row['image_name']),
                "category": str(row['category']),
                "caption": str(row['caption']),
                "material": str(row['material']),
                "style": str(row['style']),
                "score": round(item['score'], 2)
            })
            
        return final_results