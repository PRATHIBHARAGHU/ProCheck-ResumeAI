import pdfplumber
import PyPDF2
import io
import logging

logger = logging.getLogger(__name__)

class PDFParserService:
    @staticmethod
    def extract_text(file_wrapper) -> str:
        """
        Extracts raw textual strings from a validated file object using defensive strategy cascading.
        """
        file_bytes = file_wrapper.read()
        file_wrapper.seek(0) # Keep file readable downstream
        
        extracted_text = ""
        
        # Primary Attempt: pdfplumber
        try:
            with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        extracted_text += text + "\n"
        except Exception as e:
            logger.warning(f"pdfplumber pipeline execution failure, switching strategies: {e}")

        # Secondary Attempt: PyPDF2 fallback
        if not extracted_text.strip():
            try:
                reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
                for page in reader.pages:
                    text = page.extract_text()
                    if text:
                        extracted_text += text + "\n"
            except Exception as e:
                logger.error(f"PyPDF2 secondary framework analytical execution error: {e}")
                
        return extracted_text.strip()