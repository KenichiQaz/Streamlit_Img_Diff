import streamlit as st
from streamlit_image_comparison import image_comparison
import cv2
import numpy as np
from PIL import Image

if 'key' not in st.session_state:
    st.session_state['key'] = 'value'

with st.form("my-form-2", clear_on_submit=True):
    first = st.file_uploader("Choose the first file", ['png', 'jpg','jpeg'], key=1)
    second = st.file_uploader("Choose the second file", ['png', 'jpg','jpeg'], key=2)
    submitted = st.form_submit_button("Compare files")

def show_images(images):
    image1 = cv2.cvtColor(cv2.imdecode(np.frombuffer(first.read(), np.uint8), 1) , cv2.COLOR_BGR2RGB)
    image2 = cv2.cvtColor(cv2.imdecode(np.frombuffer(second.read(), np.uint8), 1) , cv2.COLOR_BGR2RGB)
    image_comparison(
        img1=image1,
        img2=image2,
        label1="Image 1",
        label2="Image 2",
    )

with st.form("my-form", clear_on_submit=True):
    images = st.file_uploader('Choose the files you want to compare', type=['png', 'jpg', 'jpeg'], accept_multiple_files=True, key=1)
    submitted = st.form_submit_button("Compare files")

if submitted is not None:
    show_images(images)
else:
    st.write('add files')

if st.button('Restart the program'):
    for key in st.session_state.keys():
        del st.session_state[key]
    st.experimental_rerun()
