import streamlit as st
import tempfile
from pathlib import Path

from integration import analyze_image
from risk_score import calculate_overall_risk

st.set_page_config(
    page_title="AI Before You Share",
    page_icon="🔐",
    layout="centered"
)

st.title("🔐 AI Before You Share")

st.write(
    "Upload an image to detect sensitive personal information "
    "before you share it."
)

uploaded_file = st.file_uploader(
    "Upload an image",
    type=["png", "jpg", "jpeg"]
)

if uploaded_file is not None:
    st.image(
        uploaded_file,
        caption="Uploaded Image",
        use_container_width=True
    )

    with tempfile.TemporaryDirectory() as temp_dir:
        image_path = Path(temp_dir) / uploaded_file.name
        image_path.write_bytes(uploaded_file.getvalue())

        with st.spinner("Analyzing image..."):
            results = analyze_image(image_path)

    overall_risk = calculate_overall_risk(results)

    st.subheader("Privacy Risk")

    st.write(
        f"Overall Risk Score: "
        f"{overall_risk['overall_risk_score']}/100"
    )

    st.write(
        f"Risk Level: "
        f"{overall_risk['overall_risk_level'].upper()}"
    )

    st.subheader("Detected Sensitive Information")

    if results:
        for item in results:
            st.write(
                f"**{item['final_type']}** — "
                f"{item['text']} — "
                f"Risk: {item['risk_score']}/100 "
                f"({item['risk_level']})"
            )
    else:
        st.success("No sensitive information detected.")