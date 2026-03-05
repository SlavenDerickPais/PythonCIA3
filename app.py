import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.set_page_config(page_title="Leaf Health Checker", page_icon="🍃")
st.title("🌿 Simple Leaf Disease Detector")
st.write("Using Basic HSV Color Thresholding")

uploaded_file = st.file_uploader("Upload a leaf image...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # --- 1. Load Image ---
    image = Image.open(uploaded_file)
    img = np.array(image)
    img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # --- 2. Process for Detection ---
    # Blur to reduce noise
    blurred = cv2.GaussianBlur(img_bgr, (5, 5), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # Define color ranges for "Diseased" spots (Brown/Yellow)
    # Adjust these values if your specific leaves are different!
    lower_disease = np.array([10, 50, 50])   # Lower Hue for Brown/Yellow
    upper_disease = np.array([30, 255, 255]) # Upper Hue for Brown/Yellow

    # Create the Threshold Mask
    mask = cv2.inRange(hsv, lower_disease, upper_disease)

    # Clean up the mask (remove tiny dots)
    kernel = np.ones((5,5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    # --- 3. UI Display ---
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Original Image")
        st.image(image, use_container_width=True)
    
    with col2:
        st.subheader("Disease Segmentation")
        # Display the black/white threshold mask
        st.image(mask, caption="White = Detected Spots", use_container_width=True)

    # --- 4. Calculation ---
    disease_pixels = cv2.countNonZero(mask)
    total_pixels = mask.shape[0] * mask.shape[1]
    severity = (disease_pixels / total_pixels) * 100

    st.divider()
    st.metric("Estimated Infection Severity", f"{severity:.2f}%")

    if severity > 5:
        st.error(" Potential disease detected. Action may be required.")
    else:
        st.success(" Leaf looks healthy!")