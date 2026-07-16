"""Main entry point for the Streamlit web application of the AI Research Assistant."""

import streamlit as st
from utils import inject_custom_css, format_file_size
from pdf_processor import extract_text_from_pdf
from ai_service import generate_response, generate_summary_sections

# Set up page configurations first
st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject custom CSS stylesheet for premium typography, spacing, and cards
inject_custom_css()

# ==========================================
# SIDEBAR SETUP
# ==========================================
# Sidebar header and branding
st.sidebar.markdown("# 🔬 AI Research Assistant")
st.sidebar.markdown("---")

# Upload PDF Button
uploaded_file = st.sidebar.file_uploader(
    "Upload a PDF Research Paper", 
    type=["pdf"], 
    help="Upload a scientific or technical document in PDF format to start analyzing."
)

st.sidebar.markdown("---")

# About Project Section
with st.sidebar.expander("ℹ️ About Project", expanded=True):
    st.markdown("""
    **AI Research Assistant** is a prototype dashboard designed to accelerate literature reviews and technical reading.
    
    ### Core Workflows:
    - **📄 Intelligent Summaries**: Overview of abstracts, methodologies, and findings.
    - **💬 Contextual Chat (Ask AI)**: Interactive query response tailored to the document.
    - **📝 Interactive Quizzes**: Automatically generated comprehension assessments.
    
    *Note: This prototype uses standard Streamlit components and simulated logic to run completely locally without API dependencies.*
    """)

# ==========================================
# MAIN PAGE SETUP
# ==========================================
# Main page title & header
st.title("🔬 AI Research Assistant")
st.markdown("##### *Streamlining publication analysis, summarization, and comprehension check.*")
st.markdown("---")

if uploaded_file is not None:
    # 1. Read document metadata
    file_name = uploaded_file.name
    file_size = uploaded_file.size
    
    # Extract text from the uploaded PDF using PyPDF2 with error handling
    extracted_text, success, status_message, num_pages = extract_text_from_pdf(uploaded_file)
    char_count = len(extracted_text)
    
    # 2. Reset QA state if a new file is uploaded
    if "current_file" not in st.session_state or st.session_state.current_file != file_name:
        st.session_state.current_file = file_name
        if "qa_result" in st.session_state:
            del st.session_state.qa_result
        
    # 2b. Generate and Cache AI Summaries if text extraction was successful
    if success:
        if "doc_summary" not in st.session_state or st.session_state.get("summary_file") != file_name:
            with st.spinner("🔬 AI is analyzing the document text and generating summaries..."):
                try:
                    summary_data = generate_summary_sections(extracted_text)
                    st.session_state.doc_summary = summary_data
                    st.session_state.summary_file = file_name
                except Exception as e:
                    st.error(f"⚠️ Failed to generate AI summary: {str(e)}")
                    # Fallback placeholders in case of failures
                    st.session_state.doc_summary = {
                        "executive_summary": "Error: Unable to generate executive summary due to API failure.",
                        "key_takeaways": "Error: Unable to generate key takeaways due to API failure.",
                        "important_topics": "Error: Unable to generate important topics due to API failure."
                    }
                    st.session_state.summary_file = file_name      
        
    # 3. Display Document Information Card
    status_color = "#2a9d8f" if success else "#e63946"
    status_label = "⚡ Ready for Queries" if success else "❌ Extraction Failed"
    
    st.markdown(f"""
    <div class="premium-card">
        <h3>📄 Document Information</h3>
        <div class="metadata-grid">
            <div class="metadata-item">
                <div class="metadata-label">File Name</div>
                <div class="metadata-value">{file_name}</div>
            </div>
            <div class="metadata-item">
                <div class="metadata-label">File Size</div>
                <div class="metadata-value">{format_file_size(file_size)}</div>
            </div>
            <div class="metadata-item">
                <div class="metadata-label">Total Pages</div>
                <div class="metadata-value">{num_pages} pages</div>
            </div>
            <div class="metadata-item">
                <div class="metadata-label">Character Count</div>
                <div class="metadata-value">{char_count:,} characters</div>
            </div>
            <div class="metadata-item">
                <div class="metadata-label">Status</div>
                <div class="metadata-value" style="color: {status_color}; font-weight: bold;">{status_label}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 4. Display extraction status and preview
    if success:
        st.success(f"🎉 {status_message}")
        with st.expander("🔍 View Extracted Text Preview", expanded=False):
            if extracted_text.strip():
                st.text_area("Extracted Text (Preview)", value=extracted_text[:2000] + ("..." if len(extracted_text) > 2000 else ""), height=250, disabled=True)
            else:
                st.warning("⚠️ The document has no extractable text content (it might contain only images/scans).")
    else:
        st.error(f"❌ {status_message}")
    
    # 4. Main Page Workspace Tabs
    tab_summary, tab_qa, tab_quiz = st.tabs([
        "📄 Summary Overview", 
        "💬 Grounded Q&A", 
        "📝 Comprehension Quiz"
    ])
    
    # Tab 1: Summary Overview
    with tab_summary:
        st.subheader("Generated Document Summary")
        st.info("💡 Below is the AI-generated structural breakdown of the uploaded publication, organized into detailed categories.")
        
        # Retrieve cached summary sections
        if success and "doc_summary" in st.session_state:
            summary = st.session_state.doc_summary
            
            with st.expander("📖 Executive Summary", expanded=True):
                st.markdown(summary.get("executive_summary", "No summary available."))
                
            with st.expander("🎯 Key Takeaways", expanded=False):
                st.markdown(summary.get("key_takeaways", "No takeaways available."))
                
            with st.expander("🏷️ Important Topics", expanded=False):
                st.markdown(summary.get("important_topics", "No topics available."))
        else:
            st.warning("⚠️ Document analysis is not available because text extraction failed.")
            
    # Tab 2: Grounded Q&A
    with tab_qa:
        st.subheader("Document Grounded Q&A")
        st.caption("Ask questions about the document. Gemini will respond strictly based on the extracted document text.")
        
        # User input question
        user_query = st.text_input("Enter your question:", key="qa_input_field", placeholder="e.g. What is the main objective of this study?")
        ask_button = st.button("Ask Assistant", type="primary")
        
        if ask_button and user_query:
            # Construct strict document grounding prompt
            grounded_prompt = (
                "You are an AI Research Assistant. Your task is to answer the user's question ONLY using the facts directly mentioned in the document context below.\n\n"
                "Context from the document:\n"
                "---START CONTEXT---\n"
                f"{extracted_text[:40000]}\n"
                "---END CONTEXT---\n\n"
                f"User Question: {user_query}\n\n"
                "Rules:\n"
                "1. Answer the question truthfully and concisely based ONLY on the context provided.\n"
                "2. If the context does not contain enough information to answer the question, you must respond EXACTLY with the phrase: "
                "'The uploaded document does not contain enough information to answer this question.'\n"
                "3. Do not use any outside knowledge, assumptions, or speculations."
            )
            
            with st.spinner("Gemini is searching the document..."):
                try:
                    response_text = generate_response(grounded_prompt)
                    st.session_state.qa_result = {
                        "question": user_query,
                        "answer": response_text,
                        "success": True
                    }
                except Exception as e:
                    st.error(f"⚠️ Error generating response: {str(e)}")
                    st.session_state.qa_result = {
                        "question": user_query,
                        "answer": "Error generating response. Please check your API key configuration.",
                        "success": False
                    }
                    
        # Display the current QA result inside a clean, modern card if present
        if "qa_result" in st.session_state:
            result = st.session_state.qa_result
            st.markdown("---")
            st.markdown(f"**Question:** {result['question']}")
            
            card_border_color = "#2a9d8f" if result["success"] else "#e63946"
            
            st.markdown(f"""
            <div class="premium-card" style="border-left: 5px solid {card_border_color}; margin-top: 15px;">
                <h4 style="margin-top: 0; color: {card_border_color};">💡 Answer</h4>
                <p style="font-size: 1rem; line-height: 1.6; margin-bottom: 0;">{result['answer']}</p>
            </div>
            """, unsafe_allow_html=True)
            
    # Tab 3: Comprehension Quiz
    with tab_quiz:
        st.subheader("Interactive Comprehension Check")
        st.caption("Verify your understanding of the document details with this generated check.")
        
        # We wrap in a streamlit form to manage check buttons and selections elegantly
        with st.form(key="comprehension_quiz_form"):
            st.markdown("##### **Question 1:** Which optimization factor directly reduces RAM consumption in the proposed architecture?")
            
            options = [
                "Deploying GPU-accelerated storage disks",
                "Employing garbage collection schedules and dynamic workers",
                "Encrypting memory spaces via hardware security keys",
                "Disabling standard visual styling components"
            ]
            
            selected_option = st.radio("Select the correct answer option:", options, index=None)
            submit_quiz = st.form_submit_button(label="Submit Answer")
            
            if submit_quiz:
                if selected_option == "Employing garbage collection schedules and dynamic workers":
                    st.success("🎉 **Correct!** The methodology specifically outlines dynamic worker allocations to keep system resources optimized.")
                elif selected_option is None:
                    st.warning("⚠️ Please select one of the multiple-choice options before submitting your response.")
                else:
                    st.error("❌ **Incorrect.** Hint: Check the Key Contributions section of the Summary Overview tab.")

else:
    # Landing page display when no file is uploaded yet
    st.info("👈 Please upload a PDF publication in the sidebar to start analysis.")
    
    st.markdown("""
    <div class="premium-card" style="text-align: center; padding: 40px; margin-top: 20px;">
        <h2 style="margin-top: 0;">Welcome to your AI Research Assistant 🔬</h2>
        <p style="font-size: 1.1rem; line-height: 1.6; max-width: 800px; margin: 15px auto 30px auto; color: #6C757D;">
            This prototype UI demonstrates how you can read, summarize, query, and test your knowledge of research papers in seconds. To experience the interactive tabs, upload any PDF document in the sidebar.
        </p>
        <div style="display: flex; justify-content: center; gap: 24px; flex-wrap: wrap;">
            <div style="flex: 1; min-width: 220px; max-width: 280px; background-color: rgba(128,128,128,0.03); border: 1px solid rgba(128,128,128,0.12); padding: 24px; border-radius: 12px; text-align: left;">
                <span style="font-size: 2.2rem; display: block; margin-bottom: 12px;">📁</span>
                <h4 style="margin: 0 0 8px 0; font-weight: 600;">1. Upload File</h4>
                <p style="font-size: 0.88rem; color: #6C757D; margin: 0; line-height: 1.4;">Select a local PDF file via the sidebar to start parsing.</p>
            </div>
            <div style="flex: 1; min-width: 220px; max-width: 280px; background-color: rgba(128,128,128,0.03); border: 1px solid rgba(128,128,128,0.12); padding: 24px; border-radius: 12px; text-align: left;">
                <span style="font-size: 2.2rem; display: block; margin-bottom: 12px;">📊</span>
                <h4 style="margin: 0 0 8px 0; font-weight: 600;">2. View Summary</h4>
                <p style="font-size: 0.88rem; color: #6C757D; margin: 0; line-height: 1.4;">Access automatically organized key sections and takeaways.</p>
            </div>
            <div style="flex: 1; min-width: 220px; max-width: 280px; background-color: rgba(128,128,128,0.03); border: 1px solid rgba(128,128,128,0.12); padding: 24px; border-radius: 12px; text-align: left;">
                <span style="font-size: 2.2rem; display: block; margin-bottom: 12px;">💬</span>
                <h4 style="margin: 0 0 8px 0; font-weight: 600;">3. Ask Questions</h4>
                <p style="font-size: 0.88rem; color: #6C757D; margin: 0; line-height: 1.4;">Use our dedicated chatbot interface to seek explanations.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# FOOTER SETUP
# ==========================================
st.markdown("""
<div class="custom-footer">
    Developed with ❤️ using Streamlit • AI Research Assistant Prototype v1.0
</div>
""", unsafe_allow_html=True)
