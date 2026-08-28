import json
import re
import easyocr
import numpy as np

from pathlib import Path
from PIL import Image


# Create the OCR reader once
reader = easyocr.Reader(["ar", "en"], gpu=False)

def normalize_iban_ocr(text):
    # Fix OCR reading Saudi IBAN prefix SA as A$
    text = re.sub(
        r"(?i)(?<![A-Z0-9])(?:A\$|\$A)(?=\s*(?:\d[\s-]*){22}(?!\d))",
        "SA",
        text
    )
    return text

def run_ocr(image_path):
    """
    Extract text, confidence score, and bounding boxes from an image.
    """

    image_path = Path(image_path)

    if not image_path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    # Open image safely and convert it to a format EasyOCR can read
    image = Image.open(image_path).convert("RGB")
    image = np.array(image)

    # Run OCR
    results = reader.readtext(image)

    detections = []

    for box, text, confidence in results:
        normalized_text = normalize_iban_ocr(text)

        # Convert NumPy numbers to normal Python integers
        clean_box = [
            [int(x), int(y)]
            for x, y in box
        ]

        detections.append({
            "text": normalized_text,
            "confidence": round(float(confidence), 3),
            "box": clean_box
        })

    return detections


if __name__ == "__main__":

    test_image = Path(__file__).parent / "test_images" / "test.png"

    detections = run_ocr(test_image)

    print(
        json.dumps(
            detections,
            ensure_ascii=False,
            indent=2
        )
    )