import streamlit as st
import tempfile
from pathlib import Path

from integration import analyze_image
from risk_score import calculate_overall_risk
from redactor import redact_image

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
        temp_dir = Path(temp_dir)

        image_path = temp_dir / uploaded_file.name
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

            st.subheader("Redaction Method")

            redaction_mode = st.radio(
                "Choose how to hide sensitive information:",
                options=["blur", "black"],
                format_func=lambda x: "Blur" if x == "blur" else "Black Box"
            )

            if st.button("Make Safe to Share"):
                output_path = temp_dir / f"safe_to_share_{redaction_mode}.jpg"

                with st.spinner("Applying redaction..."):
                    redacted_image_path = redact_image(
                        image_path=image_path,
                        output_path=str(output_path),
                        mode=redaction_mode,
                        detections=results
                    )

                st.subheader("Safe-to-Share Image")

                st.image(
                    str(redacted_image_path),
                    caption=f"Redacted Image ({redaction_mode})",
                    use_container_width=True
                )

                with open(redacted_image_path, "rb") as file:
                    st.download_button(
                        label="Download Safe Image",
                        data=file,
                        file_name=Path(redacted_image_path).name,
                        mime="image/jpeg"
                    )

        else:
            st.success("No sensitive information detected.")