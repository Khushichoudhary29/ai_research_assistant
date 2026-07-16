"""Utility helper functions for layout, styling, and general operations."""

import streamlit as st

def inject_custom_css():
    """Injects custom CSS styles to give the Streamlit application a clean, modern UI."""
    custom_css = """
    <style>
    /* Adjust top padding of the main container */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Premium Styled Card Container */
    .premium-card {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(128, 128, 128, 0.2);
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        backdrop-filter: blur(10px);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .premium-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.08);
        border-color: rgba(128, 128, 128, 0.35);
    }
    
    /* Style headings inside premium cards */
    .premium-card h3 {
        margin-top: 0 !important;
        font-weight: 600;
        color: #2F3E46;
    }
    
    /* Dark mode adjustments for card background and text */
    @media (prefers-color-scheme: dark) {
        .premium-card {
            background-color: rgba(30, 34, 42, 0.6);
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
        }
        .premium-card h3 {
            color: #E9ECEF;
        }
    }
    
    /* Metadata Grid styling */
    .metadata-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 16px;
        margin-top: 10px;
    }
    
    .metadata-item {
        background-color: rgba(0, 0, 0, 0.02);
        border: 1px solid rgba(128, 128, 128, 0.15);
        padding: 12px 16px;
        border-radius: 8px;
        font-size: 0.9rem;
    }
    
    @media (prefers-color-scheme: dark) {
        .metadata-item {
            background-color: rgba(255, 255, 255, 0.02);
        }
    }
    
    .metadata-label {
        font-weight: 600;
        font-size: 0.8rem;
        color: #6C757D;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 4px;
    }
    
    .metadata-value {
        font-weight: 500;
        color: inherit;
    }
    
    /* Footer Styling */
    .custom-footer {
        width: 100%;
        text-align: center;
        color: rgba(128, 128, 128, 0.75);
        padding: 24px 0 10px 0;
        font-size: 0.85rem;
        border-top: 1px solid rgba(128, 128, 128, 0.15);
        margin-top: 40px;
    }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)


def format_file_size(size_bytes):
    """Formats file size in bytes into a human-readable string (e.g. KB, MB)."""
    if size_bytes <= 0:
        return "0 Bytes"
    
    units = ["Bytes", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(units) - 1:
        size_bytes /= 1024.0
        i += 1
        
    return f"{size_bytes:.2f} {units[i]}"
