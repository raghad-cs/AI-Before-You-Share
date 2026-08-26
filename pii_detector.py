from transformers import pipeline

from validators import (
    validate_saudi_phone,
    validate_saudi_iban,
    validate_credit_card,
    validate_saudi_national_id,
    validate_saudi_iqama,
)


# Load OpenAI Privacy Filter
pii_detector = pipeline(
    "token-classification",
    model="openai/privacy-filter",
    aggregation_strategy="simple"
)


def refine_pii_type(text, model_type):
    """
    Refine the model prediction using structured validation rules.
    """

    if validate_saudi_iban(text):
        return "SAUDI_IBAN"

    if validate_saudi_phone(text):
        return "PRIVATE_PHONE"

    if validate_credit_card(text):
        return "CREDIT_CARD"

    if validate_saudi_national_id(text):
        return "SAUDI_NATIONAL_ID"

    if validate_saudi_iqama(text):
        return "SAUDI_IQAMA"

    # If no structured rule matches,
    # keep the original model prediction
    return model_type


def detect_pii(text):

    results = pii_detector(text)

    merged_results = []

    for result in results:

        current = {
            "text": text[result["start"]:result["end"]],
            "model_type": result["entity_group"],
            "confidence": float(result["score"]),
            "start": result["start"],
            "end": result["end"]
        }

        # Merge adjacent tokens that belong to the same PII type
        if (
            merged_results
            and current["model_type"] == merged_results[-1]["model_type"]
            and current["start"] == merged_results[-1]["end"]
        ):

            previous = merged_results[-1]

            previous["end"] = current["end"]

            previous["text"] = text[
                previous["start"]:previous["end"]
            ]

            previous["confidence"] = (
                previous["confidence"]
                + current["confidence"]
            ) / 2

        else:
            merged_results.append(current)

    # Apply validation and final classification
    for item in merged_results:

        item["confidence"] = round(
            item["confidence"], 4
        )

        item["final_type"] = refine_pii_type(
            item["text"],
            item["model_type"]
        )

    return merged_results


# -----------------------------
# Test
# -----------------------------

text = """
الاسم: رغد خالد الشاويش.
رقم الجوال: 0551234567.
البريد الإلكتروني: raghad@example.com.
رقم الآيبان: SA0380000000608010167519.
رقم الهوية: 1023456789.
رقم الإقامة: 2123456789.
رقم البطاقة: 4111111111111111.
"""

results = detect_pii(text)

for item in results:
    print(item)