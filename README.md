# ✨ Jewellery RAG-based Recommendation System

A state-of-the-art **Retrieval-Augmented Generation (RAG)** system designed for the jewellery industry. This project enables users to find their perfect jewellery piece using seamless **Natural Language Search** and **Multimodal Image-to-Search** capabilities.

---

## 🚀 Key Features

- **🔍 Hybrid Semantic Search**: Combines top-tier vector embeddings with keyword-based heuristic scoring for pinpoint accuracy.
- **📸 Multimodal Image Analysis**: Upload a jewellery photo to trigger a deep-vision analysis that identifies material, style, and intricate details.
- **🖌️ OCR-Enhanced Retrieval**: Automatically detects and extracts text/branding from jewellery images to refine search results.
- **⚡ High-Performance FAISS Backend**: Blazing-fast similarity search across thousands of products using Facebook AI Similarity Search.
- **🎨 Premium Web Interface**: A clean, responsive dashboard for intuitive product discovery.

---

## 🛠️ Technical Architecture

### **The Tech Stack**
| Layer | Technologies |
| :--- | :--- |
| **Backend** | Python, FastAPI, Uvicorn |
| **Vector Engine** | FAISS (Facebook AI Similarity Search) |
| **AI Models** | OpenAI Embeddings (`text-embedding-3-small`), Gemini LLM (Vision), PaddleOCR |
| **Data Handling** | Pandas, NumPy, Pillow |
| **Frontend** | Vanilla HTML5, CSS3, JavaScript (ES6+) |

### **How it Works**
1. **The Retrieval Loop**:
   - For a text query, the system generates a **1536-dimensional vector embedding**.
   - It performs a similarity search in the **FAISS index** to find candidate items.
   - It applies a **Hybrid Scoring Logic**: `(Vector Similarity * 0.7) + (Keyword Boost * 0.3)`.

2. **Multimodal Ingestion**:
   - When an image is uploaded, **PaddleOCR** extract labels or brand names.
   - The image is processed by a **Vision LLM (Gemini)** to generate a rich semantic description.
   - This metadata-rich description is then used as a query for the retrieval engine.

---

## 📦 Installation & Setup

### 1. Prerequisite
Ensure you have Python 3.9+ installed and an active API key for the models.

### 2. Clone and Install
```bash
# Clone the repository
git clone https://github.com/ARUN-GR05/jewellery_RAG_basedReccomendation.git
cd jewellery_RAG_basedReccomendation

# Install dependencies
pip install -r backend/requirements.txt
```

### 3. Environment Configuration
Create a `.env` file in the `backend/` directory:
```env
GPT_API_KEY=your_api_key_here
GPT_BASE_URL=your_api_base_url_here
```

### 4. Run the Application
```bash
cd backend
python main.py
```
Access the dashboard at `http://localhost:8000`.

---

## 📂 Project Structure
```text
├── backend/
│   ├── src/            # Core logic (OCR, Vision, Embedding, Search)
│   ├── data/           # FAISS index and Metadata CSV
│   ├── main.py         # FastAPI Entry point
│   └── .env            # Configuration
├── frontend/
│   ├── index.html      # UI Structure
│   ├── style.css       # Premium Styling
│   └── script.js       # Client-side Logic
└── README.md
```

---

## 🤝 Contributing
Contributions are welcome! If you have ideas for improving the recommendation accuracy or adding new vision models, feel free to open a PR.

---
*Developed with ❤️ for the Jewellery Industry.*
