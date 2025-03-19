import streamlit as st
import base64
import gzip
from io import BytesIO
from PIL import Image

def resize_image(image, max_width=800):
    width, height = image.size
    if width > max_width:
        ratio = max_width / width
        new_height = int(height * ratio)
        return image.resize((max_width, new_height))
    return image

def compress_image(image):
    # Resize the image for optimal size reduction
    resized_image = resize_image(image)

    # Convert image to bytes in WEBP format for better compression
    img_bytes = BytesIO()
    resized_image.save(img_bytes, format='WEBP', quality=75)
    img_data = img_bytes.getvalue()

    # Compress the image data
    compressed_data = gzip.compress(img_data, compresslevel=9)

    # Encode compressed data in Base85 for better size reduction than Base64
    base85_str = base64.b85encode(compressed_data).decode('utf-8')
    return base85_str

# Streamlit UI
st.title(":camera: Image to Optimized Base85 Converter")
st.markdown("Upload your image to generate a minimized Base85 string.")

uploaded_file = st.file_uploader("📂 Upload an Image", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption='📸 Uploaded Image', use_column_width=True)

    # Generate compressed Base85 string
    base85_str = compress_image(image)

    # Display the Base85 string with a copy button
    st.text_area("📝 Optimized Base85 String", base85_str, height=200)

    # Option to download the Base85 string as a text file
    b85_bytes = base85_str.encode('utf-8')
    st.download_button("⬇️ Download Base85 String", data=b85_bytes, file_name="compressed_base85.txt")
