# 🔬 AI Research Assistant

AI Research Assistant is a modern, high-performance Streamlit dashboard designed to speed up scientific publication and technical document reading. By combining robust PDF ingestion with context-aware LLM reasoning powered by **Google Gemini 2.5 Flash**, the dashboard automates document structural summary parsing, interactive Q&A, and quiz comprehension assessments.

---

## 🎨 Preview & Screenshots
Below is a visual layout preview of the application landing workspace:

![Landing Workspace Screenshot](screenshots/landing_page_placeholder.png)
*(Replace this with a real screenshot of your application workspace)*

---

## ✨ Features
1. **📄 PDF Text Extraction**: Reads raw binary PDF uploads, loops page ranges, extracts text on the fly using `PyPDF2`, and handles scanned/blank pages safely.
2. **📊 Contextual Summaries**: Dynamically parses the document content to output three structured sections—*Executive Summary*, *Key Takeaways*, and *Important Topics*—displayed in clean collapsible cards.
3. **💬 Grounded Q&A**: Refined question answering bounded strictly to the uploaded document's context, returning a fallback notice if answers cannot be found.
4. **📝 Comprehension Quiz**: Automatically generates a 5-question multiple-choice check with interactive option selections and immediate validation banners.
5. **⚡ State Caching & Performance**: Uses Streamlit's `st.session_state` to cache summaries and quizzes, preventing repeat API requests during tab switching or Q&A runs.
6. **💎 Premium Aesthetics**: Custom CSS injecting the elegant `Outfit` typography, dropshadow container cards, transitions, and dark/light theme adjustments.

---

## 🛠️ Tech Stack
- **Frontend Framework**: [Streamlit](https://streamlit.io/) (Python-based dashboard)
- **Generative AI Platform**: [Google Gemini API](https://ai.google.dev/) via the modern `google-genai` SDK
- **Ingestion Parser**: [PyPDF2](https://pypi.org/project/PyPDF2/) (Binary PDF text extractor)
- **Environment Config**: `python-dotenv` (Secrets manager)
- **Style Engine**: Vanilla CSS injected via Streamlit markdown bindings

---

## 📁 Folder Structure
```text
ai_research_assistant/
│
├── app.py              # Main dashboard script containing layouts & tab loops
├── ai_service.py       # Gemini API caller, prompt engineering, and parsing
├── pdf_processor.py    # PyPDF2 file text ingestion and error checkers
├── utils.py            # Custom CSS styling stylesheets & size formatting utilities
│
├── requirements.txt    # Project dependencies list
├── .gitignore          # Excluded cache folders and credential files
├── .env.example        # Environment variable credentials template
└── README.md           # Repository documentation and details
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.10 or higher
- A Google Gemini API Key (Get one from [Google AI Studio](https://aistudio.google.com/))

### 1. Clone & Navigate
```bash
git clone https://github.com/Khushichoudhary29/ai_research_assistant.git
cd ai_research_assistant
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Configuration
Create a `.env` file in the project root directory:
```bash
cp .env.example .env
```
Open `.env` and configure your API key:
```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

---

## 🏃 How to Run
Launch the Streamlit server from your terminal:
```bash
streamlit run app.py
```
The application will automatically open in a new browser tab at `http://localhost:8501`.

---

## 📈 Future Improvements
- **Multi-File Support**: Allow uploading and indexing multiple publications concurrently.
- **RAG & Vector Embeddings**: Integrate a local vector store (e.g. FAISS or ChromaDB) to handle very long research books beyond standard token windows.
- **Excel/CSV Export**: Add buttons to export summaries or quiz results for offline study trackers.
- **Scanned OCR Ingestion**: Integrate Tesseract or Google Cloud Vision OCR to extract text from heavy image-only PDFs.

---

## 🎓 Learning Outcomes
- **Structured LLM Outputs**: Utilizing the `google-genai` client configurations (`response_mime_type="application/json"`) to retrieve structured data directly.
- **Streamlit Caching & Lifecycles**: Designing session-state caches to persist heavy compute/API payloads across interactive Streamlit redraw triggers.
- **Document Grounding**: Constructing prompt wrappers to enforce strict context boundaries and zero-shot fallback responses.
- **PEP8 Formatting**: Designing DRY, clean helper functions, writing modular code, and following Python coding standards.

---

## 📄 License
This project is open-source and available under the [MIT License](LICENSE).
