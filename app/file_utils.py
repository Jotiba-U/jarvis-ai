import fitz  # PyMuPDF

def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract readable text from a PDF file using PyMuPDF (fitz).
    
    Args:
        file_path (str): Path to the PDF file.
    
    Returns:
        str: Extracted text as a single string.
    """
    text_content = []

    try:
        with fitz.open(file_path) as pdf:
            for page in pdf:
                text = page.get_text("text").strip()
                if text:
                    text_content.append(text)
    except Exception as e:
        print(f"[Error] Failed to read PDF ({file_path}): {e}")
        return ""

    return "\n".join(text_content).strip()
