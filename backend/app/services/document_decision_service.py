class DocumentDecisionService:

    @staticmethod
    def decide(page: dict) -> dict:
        quality_score = page["quality_score"]
        garbage_score = page["garbage_score"]
        character_count = page["character_count"]
        has_images = page["has_images"]

        # No usable text
        if character_count == 0:
            print(has_images)
            if has_images:
                return {
                    "decision": "ocr",
                    "reason": "No extracted text and page contains images"
                }

            return {
                "decision": "review",
                "reason": "No extracted text and no images detected"
            }

        #  Strong garbage detection
        if garbage_score >= 0.7:
            return {
                "decision": "ocr",
                "reason": "Extracted text appears corrupted"
            }

        #  Good extraction
        if quality_score >= 0.75:
            return {
                "decision": "accept",
                "reason": "Text extraction quality is good"
            }

        #  Medium-quality extraction
        if quality_score >= 0.45:
            return {
                "decision": "review",
                "reason": "Text extraction quality is uncertain"
            }

        #  Poor extraction
        return {
            "decision": "ocr",
            "reason": "Text extraction quality is poor"
        }