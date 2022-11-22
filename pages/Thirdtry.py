import skimage
from skimage.util import compare_images
import streamlit as st
import numpy as np
import cv2
from pdf2image import convert_from_path, convert_from_bytes

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
    
def pdf_comparison():
    images1 = convert_from_bytes(files1,fmt="png")
    images2 = convert_from_bytes(files2,fmt="png")
  for index, image in enumerate(images1):
    img1 = images1[index]
    img2 = images2[index]
    compared = compare_images(img1, img2, method='diff')
    st.image(cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY), caption='First')
    st.image(cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY), caption='second')
    st.image(cv2.cvtColor(compared, cv2.COLOR_BGR2GRAY), caption='Diff comparison')

if images1 and images2 and submitted is not None:
    st.write('Comparing files')
    pdf_comparison()
