import cv2
import numpy as np

from integration import analyze_image

def is_rtl_text(text):
    for char in text:
        if "\u0600" <= char <= "\u06FF":
            return True

        if char.isalpha():
            return False

    return False

def is_mixed_text(text):
    has_arabic = any(
        "\u0600" <= char <= "\u06FF"
        for char in text
    )

    has_ltr = any(
        char.isascii() and char.isalnum()
        for char in text
    )

    return has_arabic and has_ltr

def get_sensitive_box(detection):
    """
    Calculate the box of only the sensitive part
    inside the full OCR bounding box.
    """

    full_text = detection["ocr_text"]
    start = detection["start"]
    end = detection["end"]

    box = np.array(
        detection["box"],
        dtype=np.float32
    )

    text_length = len(full_text)

    if text_length == 0:
        return box.astype(np.int32)

    # Get the four corners of the OCR box
    top_left, top_right, bottom_right, bottom_left = box

    # Calculate the position of the sensitive text
    # inside the full OCR text
    if is_rtl_text(full_text):
        start_ratio = 1 - (end / text_length)
        end_ratio = 1 - (start / text_length)
    else:
        start_ratio = start / text_length
        end_ratio = end / text_length

    # Special handling for mixed Arabic + LTR text
    if is_mixed_text(full_text):

        # Mixed email
        if start == 0:
            start_ratio = 0

            end_ratio = min(
                1,
                end_ratio + 0.18
            )

        # Mixed Arabic + phone number
        elif detection["final_type"] == "private_phone":
            end_ratio = min(
                1,
                end_ratio + 0.12
            )

    # Calculate the sensitive box
    sensitive_top_left = (
        top_left
        + (top_right - top_left) * start_ratio
    )

    sensitive_top_right = (
        top_left
        + (top_right - top_left) * end_ratio
    )

    sensitive_bottom_left = (
        bottom_left
        + (bottom_right - bottom_left) * start_ratio
    )

    sensitive_bottom_right = (
        bottom_left
        + (bottom_right - bottom_left) * end_ratio
    )

    sensitive_box = np.array(
        [
            sensitive_top_left,
            sensitive_top_right,
            sensitive_bottom_right,
            sensitive_bottom_left
        ],
        dtype=np.int32
    )

    return sensitive_box

def apply_redaction(image, sensitive_box, mode="black"):
    """
    Apply either a black box or blur
    over the sensitive region.
    """

    if mode == "black":

        cv2.fillPoly(
            image,
            [sensitive_box],
            color=(0, 0, 0)
        )

    elif mode == "blur":

        x, y, w, h = cv2.boundingRect(
            sensitive_box
        )

        region = image[
            y:y + h,
            x:x + w
        ]

        if region.size > 0:
            blurred_region = cv2.GaussianBlur(
                region,
                (51, 51),
                0
            )

            image[
                y:y + h,
                x:x + w
            ] = blurred_region

    else:
        raise ValueError(
            "Mode must be 'black' or 'blur'"
        )

    return image


def redact_image(
    image_path,
    output_path="safe_to_share.jpg",
    mode="black"
):
    """
    Detect PII in the image and redact
    only the sensitive regions.
    """

    image = cv2.imread(
        str(image_path)
    )

    if image is None:
        raise FileNotFoundError(
            f"Image not found: {image_path}"
        )

    # Get OCR + PII + validation results
    detections = analyze_image(
        image_path
    )

    # Redact every detected PII
    for detection in detections:

        sensitive_box = get_sensitive_box(
            detection
        )

        image = apply_redaction(
            image,
            sensitive_box,
            mode
        )

    cv2.imwrite(
        output_path,
        image
    )

    return output_path


if __name__ == "__main__":

    image_path ="test_images/Raghad_try.png"
    
    # Change this to "blur" to test blur
    mode = "blur"

    output_path = (
        f"safe_to_share_{mode}.jpg"
    )

    output = redact_image(
        image_path,
        output_path,
        mode
    )

    print(
        "Redacted image saved to:",
        output
    )