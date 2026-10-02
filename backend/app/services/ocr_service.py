from pdf2image import convert_from_path
import pytesseract


class OCRService:

    @staticmethod
    def extract_page(
        pdf_path: str,
        page_number: int,
        dpi: int = 300
    ) -> str:
        """
        Convert one PDF page to an image
        and extract text using Tesseract OCR.

        page_number is 1-based.
        """

        images = convert_from_path(
            pdf_path,
            dpi=dpi,
            first_page=page_number,
            last_page=page_number
        )

        if not images:
            return ""

        image = images[0]

        text = pytesseract.image_to_string(
            image
        )

        return text.strip()