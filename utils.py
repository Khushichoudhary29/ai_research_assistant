"""Utility helper functions for layout, styling, and general operations."""

import streamlit as st


def inject_custom_css():
    """
    Injects custom CSS styles into the Streamlit application page.
    
    This function modifies the global styling, including importing the modern
    Outfit font, adjusting the grid systems, customizing container cards, and
    making sure both dark and light modes look beautiful.
    """
    custom_css = """
    <style>
    /* Import modern premium Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
    
    /* Apply Font Family globally to all standard tags */
    html, body, [class*="css"], .stApp {
        font-family: 'Outfit', sans-serif !important;
    }
    
    /* Adjust top and bottom padding of the main Streamlit container */
    .block-container {
        padding-top: 2.5rem;
        padding-bottom: 2.5rem;
    }
    
    /* Premium Styled Card Container */
    .premium-card {
        background-color: rgba(255, 255, 255, 0.45);
        border: 1px solid rgba(128, 128, 128, 0.18);
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
        backdrop-filter: blur(12px);
        transition: transform 0.22s cubic-bezier(0.4, 0, 0.2, 1), 
                    box-shadow 0.22s cubic-bezier(0.4, 0, 0.2, 1), 
                    border-color 0.22s ease;
    }
    
    .premium-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.06);
        border-color: rgba(128, 128, 128, 0.35);
    }
    
    /* Style headings inside premium cards */
    .premium-card h3 {
        margin-top: 0 !important;
        margin-bottom: 16px !important;
        font-weight: 600;
        font-size: 1.25rem;
        color: #2F3E46;
    }
    
    /* Dark mode adjustments for card background and text */
    @media (prefers-color-scheme: dark) {
        .premium-card {
            background-color: rgba(30, 34, 42, 0.65);
            border-color: rgba(255, 255, 255, 0.1);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        }
        .premium-card:hover {
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.35);
            border-color: rgba(255, 255, 255, 0.2);
        }
        .premium-card h3 {
            color: #F8F9FA;
        }
    }
    
    /* Metadata Grid styling */
    .metadata-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 16px;
        margin-top: 12px;
    }
    
    .metadata-item {
        background-color: rgba(0, 0, 0, 0.015);
        border: 1px solid rgba(128, 128, 128, 0.12);
        padding: 14px 18px;
        border-radius: 8px;
        font-size: 0.92rem;
        transition: background-color 0.2s ease;
    }
    
    .metadata-item:hover {
        background-color: rgba(0, 0, 0, 0.03);
    }
    
    @media (prefers-color-scheme: dark) {
        .metadata-item {
            background-color: rgba(255, 255, 255, 0.015);
            border-color: rgba(255, 255, 255, 0.08);
        }
        .metadata-item:hover {
            background-color: rgba(255, 255, 255, 0.03);
        }
    }
    
    .metadata-label {
        font-weight: 600;
        font-size: 0.76rem;
        color: #8D99AE;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        margin-bottom: 6px;
    }
    
    .metadata-value {
        font-weight: 500;
        color: inherit;
    }
    
    /* Centered Footer Styling */
    .custom-footer {
        width: 100%;
        text-align: center;
        color: rgba(128, 128, 128, 0.6);
        padding: 24px 0 12px 0;
        font-size: 0.82rem;
        border-top: 1px solid rgba(128, 128, 128, 0.12);
        margin-top: 48px;
        letter-spacing: 0.2px;
    }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)


def format_file_size(size_bytes):
    """
    Formats raw file size in bytes into a clean, human-readable file size string.
    
    Parameters:
        size_bytes (int): Total bytes to format.
        
    Returns:
        str: Rounded size string appended with the correct unit (e.g. KB, MB).
    """
    if size_bytes <= 0:
        return "0 Bytes"
    
    units = ["Bytes", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(units) - 1:
        size_bytes /= 1024.0
        i += 1
        
    return f"{size_bytes:.2f} {units[i]}"
