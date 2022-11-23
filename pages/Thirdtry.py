import skimage
from skimage.util import compare_images
import streamlit as st
import numpy as np
import cv2
import pdf2image

if 'key' not in st.session_state:
    st.session_state['key'] = 'value'

if st.button('Restart the program'):
    for key in st.session_state.keys():
        del st.session_state[key]
    st.experimental_rerun()

with st.form("my-form3", clear_on_submit=True):
    files1 = st.file_uploader("Choose the first file", ['pdf'], key=5)
    files2 = st.file_uploader("Choose the second file", ['pdf'], key=6)
    submitted = st.form_submit_button("Compare files")

def convert_pdf_to_image(document, dpi):
    images = []
    images.extend(list(map(lambda image: cv2.cvtColor(np.asarray(image), code=cv2.COLOR_RGB2BGR),pdf2image.convert_from_path(document, dpi=dpi),)))
    return images
    
def pdf_comparison():
    for index, image in enumerate(images1):
        st.image(image, use_column_width=True)
        img1 = image
        img2 = images2[index]
        st.write(index)
        compared = compare_images(img1, img2, method='diff')
        st.image(cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY), caption='First')
        st.image(cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY), caption='second')
        st.image(cv2.cvtColor(compared, cv2.COLOR_BGR2GRAY), caption='Diff comparison')

if files1 and files2 and submitted is not None:
    st.write('Comparing files')
    if files1.type == "application/pdf":
        images1 = pdf2image.convert_from_bytes(files1.read())
    if files2.type == "application/pdf":
        images2 = pdf2image.convert_from_bytes(files2.read())
    pdf_comparison()
