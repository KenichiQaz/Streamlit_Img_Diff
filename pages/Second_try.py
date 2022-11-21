import streamlit as st
from streamlit_image_comparison import image_comparison
import cv2
import numpy as np

if 'key' not in st.session_state:
    st.session_state['key'] = 'value'

images = []

def show_images(images):
    image_comparison(
        img1=cv2.cvtColor(cv2.imdecode(np.frombuffer(images[0].read(), np.uint8), 1) , cv2.COLOR_BGR2RGB),
        img2=cv2.cvtColor(cv2.imdecode(np.frombuffer(images[1].read(), np.uint8), 1) , cv2.COLOR_BGR2RGB),
        label1="Image 1",
        label2="Image 2",
    )

with st.form("my-form", clear_on_submit=True):
    images = st.file_uploader('Choose the files you want to compare', type=['png', 'jpg'], accept_multiple_files=True, key=1)
    submitted = st.form_submit_button("Compare files")

if submitted is not None:
    show_images(images)
else:
    st.write('add files')

if st.button('Restart the program'):
    for key in st.session_state.keys():
        del st.session_state[key]
    st.experimental_rerun()