import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.set_page_config(page_title="Leaf Health Checker", page_icon="🍃", layout="wide")

st.title("🌿 Leaf Disease Detector")
st.markdown("Upload a **leaf image** and detect potential disease spots using HSV color segmentation.")

# Sidebar Controls
st.sidebar.header("⚙ Detection Settings")

lower_h = st.sidebar.slider("Lower Hue", 0, 179, 10)
upper_h = st.sidebar.slider("Upper Hue", 0, 179, 30)

lower_s = st.sidebar.slider("Lower Saturation", 0, 255, 50)
upper_s = st.sidebar.slider("Upper Saturation", 0, 255, 255)

lower_v = st.sidebar.slider("Lower Value", 0, 255, 50)
upper_v = st.sidebar.slider("Upper Value", 0, 255, 255)

uploaded_file = st.file_uploader("📤 Upload a Leaf Image", type=["jpg", "jpeg", "png"])

if uploaded_file:

    image = Image.open(uploaded_file)
    img = np.array(image)
    img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # Blur
    blurred = cv2.GaussianBlur(img_bgr, (5, 5), 0)

    # HSV
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    lower_disease = np.array([lower_h, lower_s, lower_v])
    upper_disease = np.array([upper_h, upper_s, upper_v])

    mask = cv2.inRange(hsv, lower_disease, upper_disease)

    kernel = np.ones((5,5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    # Highlight detected disease
    highlighted = img.copy()
    highlighted[mask > 0] = [255, 0, 0]  # Red spots

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Original Leaf")
        st.image(image, use_container_width=True)

    with col2:
        st.subheader("Disease Mask")
        st.image(mask, caption="White = Suspected Disease", use_container_width=True)

    with col3:
        st.subheader("Highlighted Disease")
        st.image(highlighted, use_container_width=True)

    # Severity calculation
    disease_pixels = cv2.countNonZero(mask)
    total_pixels = mask.shape[0] * mask.shape[1]
    severity = (disease_pixels / total_pixels) * 100

    st.divider()

    st.subheader("📊 Infection Analysis")

    st.metric("Estimated Infection Severity", f"{severity:.2f}%")

    st.progress(int(severity))

    if severity < 3:
        st.success("🌱 Leaf looks healthy")
    elif severity < 8:
        st.warning("⚠ Mild infection detected")
    else:
        st.error("🚨 Significant disease detected")

    # Download result
    import io

# Convert result image to PNG buffer
buf = io.BytesIO()
result_image.save(buf, format="PNG")
byte_im = buf.getvalue()

st.download_button(
    label="⬇ Download Highlighted Result",
    data=byte_im,
    file_name="disease_result.png",
    mime="image/png"
)
