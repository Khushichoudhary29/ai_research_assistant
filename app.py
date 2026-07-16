"""Main entry point for the Streamlit web application of the AI Research Assistant."""

import streamlit as st
from utils import inject_custom_css, format_file_size
from pdf_processor import extract_text_from_pdf
from ai_service import generate_response

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
    
    # 2. Reset Chat History if a new file is uploaded
    if "current_file" not in st.session_state or st.session_state.current_file != file_name:
        st.session_state.current_file = file_name
        st.session_state.messages = [
            {
                "role": "assistant", 
                "content": f"Hello! I have completed processing the document '{file_name}' ({num_pages} pages). Ask me any specific questions about its results, methodologies, or findings!"
            }
        ]
        
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
    tab_summary, tab_ask_ai, tab_quiz = st.tabs([
        "📄 Summary Overview", 
        "💬 Ask AI Chat", 
        "📝 Comprehension Quiz"
    ])
    
    # Tab 1: Summary Overview
    with tab_summary:
        st.subheader("Generated Document Summary")
        st.info("💡 Below is an AI-generated structural breakdown of the uploaded publication.")
        
        # Display summary in two clean columns
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### 📖 Executive Abstract
            This paper presents a scalable architecture designed to address high latency and resource overhead constraints in real-time inference processing. The proposed methodology introduces a decoupled data polling engine working alongside dynamic worker allocation, aiming to achieve faster turnaround times for processing large document corpuses.
            
            ### 🎯 Key Contributions & Takeaways
            - **Performance Ingress**: Benchmark runs demonstrate an average throughput improvement of 22% over vanilla solutions.
            - **Efficient Overhead**: Reduces active RAM consumption by up to 35% through garbage collection schedules.
            - **Seamless Integration**: Fully compatible with existing RESTful API servers and event-driven architectures.
            """)
            
        with col2:
            st.markdown("""
            ### 🛠️ Process & Methodology
            1. **Ingestion & Text Extraction**: Parsing files concurrently using custom layout recognition scripts.
            2. **Chunking & Indexing**: Converting text into dense embeddings and building visual references index tree.
            3. **Asynchronous Dispatch**: Offloading heavy computing tasks to background tasks while maintaining responsive UI.
            
            ### 🔮 Future Directions
            - Expanding validation to non-standard formatted scientific PDFs containing mixed tables.
            - Introducing direct integration for caching common mathematical formulas and representations.
            """)
            
    # Tab 2: Ask AI Chat
    with tab_ask_ai:
        st.subheader("Document Q&A Chatroom")
        st.caption("Ask specific questions, request mathematical proofs, or clarify conclusions below.")
        
        # Render the chat dialog history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
                
        # User input text input box
        if prompt := st.chat_input("Ask a question about the document..."):
            # Display user query
            with st.chat_message("user"):
                st.write(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Construct a structured prompt providing the document context to Gemini
            prompt_with_context = (
                f"You are a helpful AI Research Assistant analyzing the uploaded document '{file_name}'.\n\n"
                f"Here is the text context extracted from the document:\n"
                f"---START CONTEXT---\n"
                f"{extracted_text[:40000]}\n"
                f"---END CONTEXT---\n\n"
                f"User Question: {prompt}\n\n"
                f"Please answer the user's question accurately and clearly, relying on the text context provided above."
            )
            
            # Request real response from Gemini API inside a spinner
            with st.spinner("Assistant is analyzing and typing..."):
                try:
                    response_text = generate_response(prompt_with_context)
                except Exception as e:
                    st.error(f"⚠️ Error generating response: {str(e)}")
                    response_text = "I encountered an error while trying to process your request. Please check your Gemini API key configuration and try again."
            
            # Display assistant reply
            with st.chat_message("assistant"):
                st.write(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})
            
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
