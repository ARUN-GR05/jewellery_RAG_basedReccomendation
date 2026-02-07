from openai import OpenAI
import numpy as np
import os
import json

# Initialize OpenAI client
GPT_API_KEY = os.getenv("GPT_API_KEY")
GPT_BASE_URL = os.getenv("GPT_BASE_URL")

client = None
if GPT_API_KEY:
    client = OpenAI(api_key=GPT_API_KEY, base_url=GPT_BASE_URL)

def get_embedding(text):
    """
    Generate 1536-dimensional embedding vector using OpenAI API.
    """
    if not client:
        raise ValueError("GPT_API_KEY not set. Cannot generate embeddings without API key.")
    
    try:
        response = client.embeddings.create(
            input=text,
            model="text-embedding-3-small"  # Changed to model accessible by your API key
        )
        embedding = np.array(response.data[0].embedding, dtype='float32')
        return embedding
    except Exception as e:
        print(f"Embedding Error: {e}")
        raise

def rerank_with_titan(query, candidates):
    """
    Rerank candidates using AWS Titan reranking model via OpenAI-compatible API.
    
    Args:
        query: Search query text
        candidates: List of candidate texts to rerank
    
    Returns:
        List of (index, score) tuples sorted by relevance score (highest first)
    """
    if not client:
        print("Warning: API client not available, skipping reranking")
        return [(i, 1.0) for i in range(len(candidates))]
    
    try:
        # Use OpenAI API to call reranking model
        # Format the request as a completion task
        prompt = f"""Rerank the following items based on relevance to the query: "{query}"

Items:
"""
        for i, candidate in enumerate(candidates):
            prompt += f"{i+1}. {candidate}\n"
        
        prompt += "\nReturn only the ranking as a JSON array of indices (0-based), ordered from most to least relevant."
        
        response = client.chat.completions.create(
            model="gpt-4.1-nano",  # Using available model for reranking
            messages=[
                {"role": "system", "content": "You are a reranking assistant. Return only valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )
        
        # Parse the response
        result_text = response.choices[0].message.content.strip()
        # Extract JSON array from response
        if '[' in result_text and ']' in result_text:
            start = result_text.index('[')
            end = result_text.rindex(']') + 1
            ranking = json.loads(result_text[start:end])
            
            # Convert to (index, score) format with decreasing scores
            reranked = [(idx, 1.0 - (i * 0.1)) for i, idx in enumerate(ranking)]
            return reranked
        else:
            print(f"Warning: Could not parse reranking response: {result_text}")
            return [(i, 1.0) for i in range(len(candidates))]
            
    except Exception as e:
        print(f"Reranking Error: {e}")
        # Return original order if reranking fails
        return [(i, 1.0) for i in range(len(candidates))]