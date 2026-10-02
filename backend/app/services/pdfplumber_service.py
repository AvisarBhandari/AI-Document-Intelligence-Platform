import pdfplumber


class PDFPlumberService:

    @staticmethod
    def extract_page(pdf_path: str, page_number: int) -> str:
        """
        Extract text from a single PDF page using pdfplumber.

        page_number is 1-based.
        """

        with pdfplumber.open(pdf_path) as pdf:
            page = pdf.pages[page_number - 1]

            text = page.extract_text()

            return text or ""