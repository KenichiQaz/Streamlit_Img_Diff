import streamlit as st
from streamlit_image_comparison import image_comparison
from skimage.metrics import structural_similarity
import cv2
import numpy as np

if 'key' not in st.session_state:
    st.session_state['key'] = 'value'

with st.form("my-form", clear_on_submit=False):
    first_image = st.file_uploader("Choose the first file", ['png', 'jpg'], key=1)
    second_image = st.file_uploader("Choose the second file", ['png', 'jpg'], key=2)
    submitted = st.form_submit_button("Compare files")

def img_compare(before, after):
    if before.shape != after.shape:
        st.write("The files don't have the same dimentions. Resizing the second image to match the first.")
    before_gray = cv2.cvtColor(before, cv2.COLOR_BGR2GRAY)
    after_gray = cv2.cvtColor(after, cv2.COLOR_BGR2GRAY)
    (score, diff) = structural_similarity(before_gray, after_gray, full=True)
    print("Image Similarity: {:.4f}%".format(score * 100))

    diff = (diff * 255).astype("uint8")

    thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]
    mask = np.zeros(before.shape, dtype='uint8')
    filled_after = after.copy()
    for c in contours:
        area = cv2.contourArea(c)
        if area > 40:
            cv2.drawContours(mask, [c], 0, (255,255,255), -1)
            cv2.drawContours(filled_after, [c], 0, (0,255,0), -1)
    
    image_comparison(img1=before, img2=after,
                             label1='First document',
                             label2='Second document')
    st.image(filled_after, caption='Differance comparison in white')

if first_image and second_image and submitted is not None:
    before = cv2.cvtColor(cv2.imdecode(np.frombuffer(first_image.read(), np.uint8), 1) , cv2.COLOR_BGR2RGB)
    after = cv2.cvtColor(cv2.imdecode(np.frombuffer(second_image.read(), np.uint8), 1) , cv2.COLOR_BGR2RGB)
    st.write('Comparing files')
    img_compare(before, after)

if st.button('Restart the program'):
    for key in st.session_state.keys():
        del st.session_state[key]
    st.experimental_rerun()