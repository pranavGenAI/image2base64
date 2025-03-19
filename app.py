import streamlit as st
import base64
import gzip
from io import BytesIO
from PIL import Image

# Custom styling
st.markdown("""
    <style>
        .main {background-color: #f0f2f6;}
        .stButton>button {background-color: #4CAF50; color: white; font-weight: bold; border-radius: 8px; padding: 10px 24px;}
        .stTextArea>div>textarea {font-family: monospace;}
    </style>
""", unsafe_allow_html=True)

def compress_image(image):
    # Convert image to bytes
    img_bytes = BytesIO()
    image.save(img_bytes, format='PNG')  # Use PNG for lossless compression
    img_data = img_bytes.getvalue()

    # Compress the image data
    compressed_data = gzip.compress(img_data)

    # Encode compressed data in Base64
    base64_str = base64.b64encode(compressed_data).decode('utf-8')
    return base64_str

# Streamlit UI
st.title(":camera: Image to Compressed Base64 Converter")
st.markdown("Upload your image to generate a minimized Base64 string.")

uploaded_file = st.file_uploader("📂 Upload an Image", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption='📸 Uploaded Image', use_column_width=True)

    # Generate compressed Base64 string
    base64_str = compress_image(image)

    # Display the Base64 string with a copy button
    st.text_area("📝 Compressed Base64 String", base64_str, height=200)

    # Option to download the Base64 string as a text file
    b64_bytes = base64_str.encode('utf-8')
    st.download_button("⬇️ Download Base64 String", data=b64_bytes, file_name="compressed_base64.txt")
