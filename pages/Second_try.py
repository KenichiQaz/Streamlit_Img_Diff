import streamlit as st
from streamlit_image_comparison import image_comparison

images = []

def upload_images():
    images = st.file_uploader('Choose the files you want to compare', type=['png', 'jpg'], accept_multiple_files=True)
    show_images(images)

def show_images(images):
    image_comparison(
        img1=images[0],
        img2=images[1],
        label1="Image 1",
        label2="Image 2",
    )