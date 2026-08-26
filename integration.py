from pathlib import Path

from ocr import run_ocr
from pii_detector import detect_pii


def analyze_image(image_path):
    """
    Run OCR on the image, then send each extracted text
    segment to the PII detector.
    """

    # Step 1: OCR
    ocr_results = run_ocr(image_path)

    final_results = []

    # Step 2: Send each OCR text segment to the PII detector
    for ocr_item in ocr_results:

        extracted_text = ocr_item["text"]

        pii_results = detect_pii(extracted_text)

        # Step 3: Combine OCR + PII results
        for pii_item in pii_results:

            final_results.append({
                "text": pii_item["text"],
                "model_type": pii_item["model_type"],
                "final_type": pii_item["final_type"],

                "ocr_confidence": ocr_item["confidence"],
                "pii_confidence": pii_item["confidence"],

                "box": ocr_item["box"],

                "start": pii_item["start"],
                "end": pii_item["end"]
            })

    return final_results


if __name__ == "__main__":

    test_image = (
        Path(__file__).parent
        / "test_images"
        / "test.png"
    )

    results = analyze_image(test_image)

    for item in results:
        print(item)