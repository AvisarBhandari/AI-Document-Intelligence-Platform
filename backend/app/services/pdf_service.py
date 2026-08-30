import re
from pathlib import Path

from pypdf import PdfReader

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
        text = page["text"]

        character_count = page["character_count"]
        word_count = page["word_count"]

        garbage_result = PDFService.detect_garbage_text(text)

        if character_count == 0:
            quality = "bad"

        elif garbage_result["is_garbage"]:
            quality = "garbage"

        elif character_count < 50 or word_count < 10:
            quality = "poor"

        else:
            quality = "good"

        return {
            **page,
            "quality": quality,
            "garbage_score": garbage_result["garbage_score"],
            "garbage_reason": garbage_result["reason"],
            "is_garbage": garbage_result["is_garbage"]
        }

    
    @staticmethod
    def analyze_pdf(pdf_path: str) -> list[dict]:
        pages = PDFService.extract_pages(pdf_path)

        analyzed_pages = []

        for page in pages:
            analyzed_page = PDFService.analyze_page_quality(page)
            analyzed_pages.append(analyzed_page)

        return analyzed_pages

