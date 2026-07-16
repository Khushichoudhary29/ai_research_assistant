"""Module containing utility functions for parsing and extracting content from PDF documents."""

import PyPDF2


def extract_text_from_pdf(file_stream):
    """
    Extracts all text content from an uploaded PDF file stream using PyPDF2.
    
    Parameters:
        file_stream (BytesIO or similar): The binary file-like object of the uploaded PDF.
        
    Returns:
        tuple: (extracted_text, success, message, num_pages)
            - extracted_text (str): The concatenated text content from all pages.
            - success (bool): True if extraction succeeded without parsing errors, False otherwise.
            - message (str): Status description indicating success details or specific error messages.
            - num_pages (int): The total number of pages in the PDF document.
    """
    extracted_pages = []
    
    try:
        # Initialize the PDF reader from the uploaded file stream.
        # PyPDF2.PdfReader reads binary streams directly.
        pdf_reader = PyPDF2.PdfReader(file_stream)
        
        # Retrieve the total page count from the document.
        num_pages = len(pdf_reader.pages)
        
        # Iterate over each page index to extract its textual content.
        for page_idx in range(num_pages):
            page = pdf_reader.pages[page_idx]
            
            # Extract text from the current page.
            # page.extract_text() returns a string, or an empty string/None if no text is found.
            page_text = page.extract_text()
            
            # Handle empty pages safely.
            if page_text:
                extracted_pages.append(page_text)
            else:
                # For scanned documents, image-only pages, or blank pages, we append an empty string.
                extracted_pages.append("")
                
        # Concatenate text from all pages into a single cohesive string.
        full_text = "\n".join(extracted_pages)
        
        # Return the final extracted string along with a success flag, message, and page count.
        return full_text, True, f"Successfully extracted text from all {num_pages} pages.", num_pages
        
    except PyPDF2.errors.PdfReadError as e:
        error_msg = (
            f"Corrupted PDF Error: The uploaded file structure is invalid.\n\n"
            f"Suggestions:\n"
            f"1. Please verify that this is a valid, uncorrupted PDF document.\n"
            f"2. Check if the file is encrypted or password-protected.\n"
            f"3. Try re-exporting the document and upload it again.\n\n"
            f"Technical Details: {str(e)}"
        )
        return "", False, error_msg, 0
        
    except Exception as e:
        error_msg = (
            f"Unexpected Ingestion Error: Unable to read PDF document.\n\n"
            f"Suggestions:\n"
            f"1. Ensure the file stream is not empty or closed.\n"
            f"2. Verify you have read permissions for the source file.\n\n"
            f"Technical Details: {str(e)}"
        )
        return "", False, error_msg, 0
