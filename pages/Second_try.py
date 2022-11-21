import streamlit as st
import cv2
from streamlit_image_comparison import image_comparison

st.header("J. Webb Space Telescope vs Hubble Telescope")

st.write("")
"This is a reproduction of the fantastic [WebbCompare](https://www.webbcompare.com/index.html) app by [John Christensen](https://twitter.com/JohnnyC1423). It's built in Streamlit and takes only 10 lines of Python code. If you like this app, please star [John's original repo](https://github.com/JohnEdChristensen/WebbCompare)!"
st.write("")
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