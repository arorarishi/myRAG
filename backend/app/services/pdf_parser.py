from markitdown import MarkItDown
import os
import tempfile

class PDFParser:
    def __init__(self):
        self.md = MarkItDown()

    async def parse(self, file_path: str) -> str:
        """
        Parses a PDF file and returns the content as Markdown.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        result = self.md.convert(file_path)
        return result.text_content

pdf_parser = PDFParser()

def parse_pdf(content: bytes) -> str:
    """
    Parse PDF from bytes content.
    Creates a temporary file, parses it, and returns the text.
    """
    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
        tmp_file.write(content)
        tmp_path = tmp_file.name
    
    try:
        # Parse the PDF
        md = MarkItDown()
        result = md.convert(tmp_path)
        return result.text_content
    finally:
        # Clean up the temporary file
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)

