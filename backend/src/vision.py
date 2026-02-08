import base64
from io import BytesIO
from openai import OpenAI
import os

# --- UPDATED CONFIGURATION ---
# Load both Key and Base URL from environment variables
GPT_API_KEY = os.getenv("GPT_API_KEY") # Renamed for clarity
GPT_BASE_URL = os.getenv("GPT_BASE_URL") # <--- NEW: Your Custom URL

# Initialize Client with your specific URL (only if API key is provided)
client = None
if GPT_API_KEY:
    client = OpenAI(
        api_key=GPT_API_KEY, 
        base_url=GPT_BASE_URL
    )
else:
    print("WARNING: GPT_API_KEY not set. Image vision analysis will be disabled.")
    print("Set GPT_API_KEY in environment variables to enable this feature.")

def analyze_image_with_text(image, detected_text):
    """
    Sends Image + OCR Text to your custom GPT endpoint.
    """
    if not client:
        return "Vision analysis unavailable (API key not configured). Please set GPT_API_KEY environment variable."
    
    try:
        # Convert Image to Base64
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        b64_img = base64.b64encode(buffered.getvalue()).decode('utf-8')
        
        prompt = f"""
        You are a jewellery search assistant.
        The user uploaded an image.
        OCR Text detected in image: "{detected_text}"
        
        Describe the jewellery in the image for a semantic search engine.
        1. Include Category (Ring, Necklace), Material (Gold, Silver), and Style.
        2. If the OCR text is a brand or specific detail, include it.
        3. Output ONLY the description.
        """
        
        response = client.chat.completions.create(
            # Switch to available vision model
            model="gemini-1.5-flash", 
            messages=[
                {"role": "user", "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64_img}"}}
                ]}
            ],
            max_tokens=300
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Vision Error: {e}")
        # Return error details to help debugging, or fallback to OCR if available
        if detected_text and len(detected_text) > 5:
             return f"Jewellery item with text: {detected_text}"
        return "Jewellery piece with specific design elements."