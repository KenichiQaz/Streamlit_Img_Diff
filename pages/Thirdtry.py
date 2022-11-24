import streamlit as st
import numpy as np
import cv2
import pdf2image
from streamlit_image_comparison import image_comparison
import torch
import torchvision
import torchvision.transforms.functional as F
from PIL import Image

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

def tint_green(totint):
    green = F.adjust_hue(Image.fromarray(totint), hue_factor=0.3)
    return green

def convert_pdf_to_image(document, dpi):
    images = []
    images.extend(list(map(
        lambda image: cv2.cvtColor(np.asarray(image),
        code=cv2.COLOR_RGB2BGR),
        pdf2image.convert_from_path(document, dpi=dpi),)))
    return images

def mse(img1, img2):
    h, w, c = img1.shape
    diff = cv2.subtract(img1, img2)
    err = np.sum(diff**2)
    error = err/(float(h*w))
    return error, diff

def pdf_comparison():
    for index, image in enumerate(images1):
        imag1 = np.array(image)
        imag2 = np.array(images2[index])
        error, diff = mse(imag1, imag2)
        if error > 0:
            mess = "On page: "+ str(index)+ " there was an difference of "+ "{:.1f}".format(error)+"%"
            st.write(mess)
            image_comparison(
                img1=imag1,
                img2=imag2,
                label1="First document",
                label2="Second document",
            )
            st.image(tint_green(diff), caption='Differance comparison in white')
            

if files1 and files2 and submitted is not None:
    if files1.type == "application/pdf":
        images1 = pdf2image.convert_from_bytes(files1.read())
    if files2.type == "application/pdf":
        images2 = pdf2image.convert_from_bytes(files2.read())
    pdf_comparison()
