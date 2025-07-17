import streamlit as st
from google.generativeai import GenerativeModel
import google.generativeai as genai
from PIL import Image
import io

# 🔐 Configure Gemini API
genai.configure(api_key="AIzaSyDYNOe66OqjEg9dDg_gQHsBB3DHj8YJGr0")
model = GenerativeModel("gemini-2.0-flash")

# 🖼️ Streamlit UI
st.set_page_config(page_title="Emotion Detector", layout="centered")
st.title("🧠 Emotion Detection with Gemini Vision")
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
# 📤 Process and send image to Gemini
if uploaded_file:
    image_bytes = uploaded_file.read()
    image = Image.open(io.BytesIO(image_bytes))  # ✅ Convert bytes to PIL.Image
    prompt = "Describe the emotional expressions in this image. in terms of happiness, sadness, anger, or any other emotions you can identify in one word only."
    with st.spinner("Analyzing emotions..."):
        response = model.generate_content([prompt, image])
    # 📝 Display GenAI interpretation
    st.subheader("🧠 Gemini Interpretation")
    st.write(response.text)
    st.image(image, caption="Uploaded Image", use_container_width =True)

