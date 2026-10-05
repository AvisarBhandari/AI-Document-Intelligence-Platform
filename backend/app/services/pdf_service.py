import re
from pathlib import Path

from pypdf import PdfReader

from services.pdfplumber_service import PDFPlumberService
from services.document_decision_service import DocumentDecisionService
from services.ocr_service import OCRService

class PDFService:
    @staticmethod
    def extract_pages(pdf_path: str) -> list[dict]:
        reader = PdfReader(pdf_path)
        pages = []

        for page_number, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            text = text.strip()
            image_count = len(page.images)

            pages.append({
                "page_number": page_number,
                "text": text,
                "character_count": len(text),
                "word_count": len(
                    re.findall(r"\b[\w'-]+\b", text)
                ),
                "image_count": image_count,
                "has_images": image_count > 0,
            })

        return pages
    @staticmethod
    def calculate_quality_score(page: dict) -> float:
        character_count = page["character_count"]
        word_count = page["word_count"]
        garbage_score = page["garbage_score"]

        # Text amount score
        if character_count == 0:
            text_amount_score = 0.0
        elif character_count < 100:
            text_amount_score = 0.3
        elif character_count < 500:
            text_amount_score = 0.6
        elif character_count < 1000:
            text_amount_score = 0.8
        else:
            text_amount_score = 1.0

        # Word quality score
        if word_count == 0:
            word_score = 0.0
        elif word_count < 10:
            word_score = 0.3
        elif word_count < 50:
            word_score = 0.6
        elif word_count < 100:
            word_score = 0.8
        else:
            word_score = 1.0

        # Character quality score
        if character_count == 0:
            character_score = 0.0
        else:
            text = page["text"]

            normal_characters = sum(
                1 for char in text
                if char.isalnum() or char.isspace()
            )

            normal_character_ratio = (
                normal_characters / character_count
            )

            character_score = min(
                max(normal_character_ratio, 0.0),
                1.0
            )

        # Garbage score
        garbage_quality_score = 1.0 - garbage_score

        # Final weighted score
        quality_score = (
            (text_amount_score * 0.30)
            + (word_score * 0.20)
            + (character_score * 0.20)
            + (garbage_quality_score * 0.30)
        )

        return round(quality_score, 2)

    
    @staticmethod
    def detect_garbage_text(text: str) -> dict:
        if not text.strip():
            return{
                "is_garbage": True,
                "garbage_score": 1.0,
                "reason": "empty_text"
            }
        words = re.findall(r"\b[\w'-]+\b", text)

        if not words:
            return{
                "is_garbage": True,
                "garbage_score": 1.0,
                "reason": "no_words_detected"
            }
        # How many token are only one character?
        single_char_words = sum(
            1 for word in words
            if len(word) == 1 and word.isalpha()
        )
        single_char_ratio = single_char_words / len(words)

        # How much of the text consists of normal letterd/numbers/whitespace?
        normal_characters = len(
            re.findall(r"[A-Za-z0-9\s]", text)
        )

        normal_character_ratio = (
            normal_characters / len(text)
            if text
            else 0
        )
        # Look for excessive repeated characters
        repeated_pattern = re.search(
            r"(.)\1{5,}",
            text
        )

        # Calculate a simple garbage score
        score = 0.0
        reasons = []

        if single_char_ratio > 0.50:
            score += 0.5
            reasons.append("too_many_single_character_words")

        if normal_character_ratio < 0.50:
            score += 0.3
            reasons.append("too_many_unusual_characters")

        if repeated_pattern:
            score += 0.2
            reasons.append("repeated_character_pattern")

        score = min(score, 1.0)

        return {
            "is_garbage": score >= 0.5,
            "garbage_score": round(score, 2),
            "reason": reasons
        }

    @staticmethod
    def analyze_page_quality(page: dict) -> dict:
        character_count = page["character_count"]
        word_count = page["word_count"]

        garbage_result = PDFService.detect_garbage_text(
            page["text"]
        )

        updated_page = {
            **page,
            "garbage_score": garbage_result["garbage_score"],
            "garbage_reason": garbage_result["reason"],
            "is_garbage": garbage_result["is_garbage"]
        }

        quality_score = PDFService.calculate_quality_score(
            updated_page
        )

        if quality_score >= 0.75:
            quality = "good"

        elif quality_score >= 0.45:
            quality = "poor"

        else:
            quality = "bad"

        return {
            **updated_page,
            "quality_score": quality_score,
            "quality": quality,
        }
        
    @staticmethod
    def analyze_pdf(pdf_path: str) -> list[dict]:

        pages = PDFService.extract_pages(pdf_path)

        analyzed_pages = []

        for page in pages:

            analyzed_page = PDFService.analyze_page_quality(
                page
            )
            analyzed_page["extractor"] = "pypdf"
            best_page = PDFService.choose_best_extraction(
                analyzed_page,
                pdf_path
            )
            decision = DocumentDecisionService.decide(
                best_page
            )

            best_page.update(decision)
            analyzed_pages.append(best_page)
        return analyzed_pages

    
    @staticmethod
    def choose_best_extraction(
        pypdf_page: dict,
        pdf_path: str
    ) -> dict:

        candidates = [pypdf_page]

        
        # 1. Try pdfplumber if pypdf is questionable
        
        if pypdf_page["quality_score"] < 0.75:

            alternative_text = PDFPlumberService.extract_page(
                pdf_path,
                pypdf_page["page_number"]
            )

            alternative_page = {
                **pypdf_page,
                "text": alternative_text,
                "character_count": len(alternative_text),
                "word_count": len(alternative_text.split()),
                "extractor": "pdfplumber",
            }

            alternative_page = PDFService.analyze_page_quality(
                alternative_page
            )

            alternative_page["extractor"] = "pdfplumber"

            candidates.append(alternative_page)

        
        # 2. Check best result so far
        
        best_page = max(
            candidates,
            key=lambda page: page["quality_score"]
        )

        
        # 3. Try OCR if still questionable
        
        if best_page["quality_score"] < 0.75:

            ocr_text = OCRService.extract_page(
                pdf_path,
                pypdf_page["page_number"]
            )

            ocr_page = {
                **pypdf_page,
                "text": ocr_text,
                "character_count": len(ocr_text),
                "word_count": len(ocr_text.split()),
                "extractor": "ocr",
            }

            ocr_page = PDFService.analyze_page_quality(
                ocr_page
            )

            ocr_page["extractor"] = "ocr"

            candidates.append(ocr_page)

        
        # 4. Record scores from every candidate
        
        candidate_scores = {}

        for candidate in candidates:
            candidate_scores[
                candidate["extractor"]
            ] = candidate["quality_score"]

        
        # 5. Choose the best extraction
        
        best_page = max(
            candidates,
            key=lambda page: page["quality_score"]
        )

        # Store candidate scores in final result
        best_page["candidate_scores"] = candidate_scores

        return best_page
        