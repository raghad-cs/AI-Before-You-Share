RISK_SCORES = {
    "private_person": 30,
    "private_email": 50,
    "private_phone": 70,
    "private_address": 80,
}


def get_risk_level(score):
    if score >= 70:
        return "high"
    elif score >= 40:
        return "medium"
    else:
        return "low"


def add_risk_score(detection):
    pii_type = detection.get("final_type", "").lower()

    score = RISK_SCORES.get(pii_type, 40)

    detection["risk_score"] = score
    detection["risk_level"] = get_risk_level(score)

    return detection


def calculate_overall_risk(detections):
    if not detections:
        return {
            "overall_risk_score": 0,
            "overall_risk_level": "low"
        }

    overall_score = max(
        item.get("risk_score", 0)
        for item in detections
    )

    return {
        "overall_risk_score": overall_score,
        "overall_risk_level": get_risk_level(overall_score)
    }