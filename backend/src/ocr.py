from paddleocr import PaddleOCR
import numpy as np
import logging

# Suppress debug logs
logging.getLogger("ppocr").setLevel(logging.ERROR)

# Initialize PaddleOCR on CPU
# use_angle_cls=True gives better results but uses more RAM. 
# Set to False if Render free tier runs out of memory.
ocr = PaddleOCR(use_angle_cls=True, lang='en', use_gpu=False, show_log=False)

def extract_text(image):
    """
    Extracts text from PIL Image.
    """
    try:
        image_np = np.array(image)
        result = ocr.ocr(image_np, cls=True)
        
        detected_text = []
        if result and result[0]:
            for line in result[0]:
                text = line[1][0]
                confidence = line[1][1]
                if confidence > 0.6: # Confidence threshold
                    detected_text.append(text)
        
        return " ".join(detected_text)
    except Exception as e:
        print(f"OCR Error: {e}")
        return ""