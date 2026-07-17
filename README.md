# 🔬 AI Research Assistant

AI Research Assistant is a simple and clean Streamlit application that helps you read and understand PDF research papers and technical documents. Powered by the Google Gemini API, it extracts text, generates summaries, answers questions, and creates interactive quizzes.

---

## 📸 Screenshots & Working Demo

### Application Layout
Here is the clean and modern landing page of the application:

![App Landing Page](screenshots/landing_page.png)

### Working Demo
See how the application parses PDFs and extracts information:

![App Working Demo](screenshots/working_demo.webp)

### Research Paper Analysis & Q&A Screenshots
Here are screenshots of the application analyzing the uploaded cloud security RBAC research paper and answering contextual questions:

![RBAC Paper Analysis Overview](screenshots/paper_demo.png)

![Grounded Q&A Results](screenshots/Q&A_demo.png)



## ✨ Key Features
- **📄 PDF Text Ingestion**: Upload any PDF file to extract all text content automatically.
- **📊 Auto Summarization**: Get a structured Executive Summary, Key Takeaways, and list of Important Topics.
- **💬 Grounded Q&A**: Ask questions and get answers based strictly on the document text.
- **📝 Comprehension Quiz**: Take a 5-question multiple-choice quiz to test your understanding.
- **⚡ Smart Caching**: Caches summaries and quizzes so the app remains fast and responsive.

---

## 🛠️ Tech Stack
- **Python**: Core programming language.
- **Streamlit**: Web interface framework.
- **Google Gemini API**: Generates summaries, Q&A responses, and quizzes.
- **PyPDF2**: Extracts text from PDF files.
- **python-dotenv**: Manages configuration keys.

---

## 📁 Project Structure
- [app.py](file:///c:/Users/User/.gemini/antigravity-ide/scratch/ai_research_assistant/app.py): The main Streamlit web application.
- [ai_service.py](file:///c:/Users/User/.gemini/antigravity-ide/scratch/ai_research_assistant/ai_service.py): Service code for calling the Google Gemini API.
- [pdf_processor.py](file:///c:/Users/User/.gemini/antigravity-ide/scratch/ai_research_assistant/pdf_processor.py): Utility code to extract text from PDF files.
- [utils.py](file:///c:/Users/User/.gemini/antigravity-ide/scratch/ai_research_assistant/utils.py): Styling and layout helper functions.
- [requirements.txt](file:///c:/Users/User/.gemini/antigravity-ide/scratch/ai_research_assistant/requirements.txt): List of Python packages required for the project.

---

## 🚀 How to Run the Project

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API Key
Create a file named `.env` in the project root directory and add your Google Gemini API key:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### 3. Run the application
```bash
streamlit run app.py
```

---

## 📈 Future Enhancements
- **Multi-File & Cross-Paper Analysis**: Allow uploading multiple documents and comparing methodologies, findings, or metrics across them.
- **RAG & Vector Embeddings**: Integrate a local vector store (such as ChromaDB or FAISS) to support semantic search and question answering across large textbooks or folders of publications.
- **Auto Reference Linking**: Extract cited publications and automatically fetch their abstracts or link them directly to Google Scholar / CrossRef.
- **Key Formula & LaTeX Indexing**: Identify, extract, and render complex mathematical formulas, symbols, and proof logic in standard LaTeX.
- **Voiceover Summaries (Text-to-Speech)**: Generate audio files from the Executive Summary and Key Takeaways for technical learning on the go.
- **Offline PDF OCR parsing**: Integrate Tesseract or EasyOCR engines to read and extract textual context from image-only scans and diagrams.
- **Data Exporting**: Enable downloading summaries, conversation history cards, and quiz results as Markdown, CSV, or PDF reports.


---

## 📄 License
This project is open-source and licensed under the MIT License.
