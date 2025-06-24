import streamlit as st
import openai
import base64

# Set your OpenAI API key here (or use st.secrets for security)
openai.api_key = "KEY"

st.set_page_config(page_title="Screenshot to Email HTML", layout="centered")
st.title("📧 Screenshot → Email HTML Generator")
st.write(
    "Upload an email screenshot. AI will convert it to responsive, production-ready HTML for all major email clients."
)

uploaded_file = st.file_uploader(
    "Drag & drop an image or click to upload (PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"]
)

if uploaded_file:
    st.image(uploaded_file, caption="Your uploaded screenshot", use_column_width=True)

    bytes_data = uploaded_file.read()
    b64_img = base64.b64encode(bytes_data).decode("utf-8")

    with st.spinner("Generating HTML email from your screenshot..."):
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert email HTML developer. You will be given a screenshot of an email design. Generate responsive, production-ready HTML using only table-based layout and inline styles. Ensure the code is compatible with Gmail, Outlook (including desktop versions), and Apple Mail."
                            "Important instructions:"
                            "- Do not use modern CSS features such as flexbox, grid, or external stylesheets."
                            "- Use inline CSS only."
                            "- Do not use JavaScript."
                            "- Include Outlook-specific conditional comments where needed (such as <!--[if mso]> ... <![endif]-->) to ensure correct rendering in Microsoft Outlook."
                            "- Include ALT text for images, and ensure all text is selectable (not just in images)."
                            "- Match the screenshot’s layout, typography, and spacing as closely as possible."
                            "- Output only the HTML code—no extra commentary."
                    ),
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Generate HTML for this email screenshot:"},
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64_img}"}},
                    ],
                },
            ],
        )
        html_code = response["choices"][0]["message"]["content"]

        # Save output
        with open("output_email.html", "w", encoding="utf-8") as f:
            f.write(html_code)

        st.success("HTML generated and saved as `output_email.html`.")
        st.download_button(
            label="⬇️ Download HTML",
            data=html_code,
            file_name="output_email.html",
            mime="text/html",
        )
        with st.expander("🔍 Show HTML Code"):
            st.code(html_code, language="html")
        with st.expander("📥 Preview Email"):
            st.components.v1.html(html_code, height=800, scrolling=True)

else:
    st.info("Upload an image file to begin.")

