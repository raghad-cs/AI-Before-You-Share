# AI Before You Share

**AI-powered privacy detection and redaction for images before sharing them online.**

AI Before You Share is a privacy-focused prototype that detects sensitive information in images, evaluates its privacy risk, and automatically produces a safer version using blur or black-box redaction.

## Features

- Arabic and English text extraction using EasyOCR
- PII detection using OpenAI Privacy Filter
- Saudi-specific validation for structured sensitive data
- Rule-based privacy risk scoring
- Black-box and blur redaction
- Streamlit user interface
- Safe-to-share image preview and download

## How It Works

1. The user uploads an image.
2. EasyOCR extracts Arabic and English text.
3. OpenAI Privacy Filter identifies potential PII.
4. Validation rules check supported Saudi-specific formats.
5. Each detected item receives a privacy risk score.
6. Sensitive regions are redacted using either:
   - Black Box
   - Blur
7. The protected image can be previewed and downloaded.

## Privacy Risk Scoring

The prototype uses a **rule-based privacy risk score**, not a model confidence or accuracy score.

| PII Type | Risk Score |
|---|---:|
| Person | 30 |
| Email | 50 |
| Phone | 70 |
| Address | 80 |
| Other detected PII | 40 |

Risk levels:

- **Low:** below 40
- **Medium:** 40–69
- **High:** 70 and above

The overall image risk is determined by the **highest risk score** among the detected PII items.

## Demo

### Original Image

![Original Demo](examples/original_demo.png)

### Black-Box Redaction

![Black Box Redaction](examples/redacted_black.jpg)

### Blur Redaction

![Blur Redaction](examples/redacted_blur.jpg)

> **Note:** All information shown in the demo images is synthetic and used for demonstration purposes only.

## Technologies

- Python
- EasyOCR
- OpenAI Privacy Filter
- OpenCV
- Streamlit
- Transformers
- PyTorch
- Pillow
- NumPy
- Git & GitHub

## Run the Project

Install the required dependencies:

```bash
pip install -r requirements.txt