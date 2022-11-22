import streamlit as st
import cv2
import numpy as np
from skimage.metrics import structural_similarity
from streamlit_image_comparison import image_comparison

if 'key' not in st.session_state:
    st.session_state['key'] = 'value'

st.set_page_config(page_title="Image-Comparison Example", layout="centered")

if st.button('Restart the program'):
    for key in st.session_state.keys():
        del st.session_state[key]
    st.experimental_rerun()

with st.form("my-form", clear_on_submit=True):
    first_image = st.file_uploader("Choose the first file", ['png', 'jpg'], key=3)
    second_image = st.file_uploader("Choose the second file", ['png', 'jpg'], key=4)
    submitted = st.form_submit_button("Compare files")

def img_comparison(before, after):
    image_comparison(
        img1=before,
        img2=after,
    )

if first_image and second_image and submitted is not None:
    before = cv2.cvtColor(cv2.imdecode(np.frombuffer(first_image.read(), np.uint8), 1) , cv2.COLOR_BGR2RGB)
    after = cv2.cvtColor(cv2.imdecode(np.frombuffer(second_image.read(), np.uint8), 1) , cv2.COLOR_BGR2RGB)
    st.write('Comparing files')
    img_comparison(before, after)