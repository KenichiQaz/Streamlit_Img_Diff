import streamlit as st
import cv2
import numpy as np
from streamlit_image_comparison import image_comparison
import pdf2image
from skimage.metrics import structural_similarity
mess = ''
filetypes = ["image/jpeg","image/png"]

if 'key' not in st.session_state:
    st.session_state['key'] = 'value'

st.set_page_config(page_title="Image Comparison", layout="centered")

st.title("Image Comparison (under construction)")

if st.button('Restart the program'):
    for key in st.session_state.keys():
        del st.session_state[key]
    st.experimental_rerun()

with st.form("my-form2", clear_on_submit=True):
    files1 = st.file_uploader("Choose the first file", ['png', 'jpg', 'jpeg', 'pdf'], key=3)
    files2 = st.file_uploader("Choose the second file", ['png', 'jpg', 'jpeg', 'pdf'], key=4)
    submitted = st.form_submit_button("Compare files")

def convert_pdf_to_image(document, dpi):
    images = []
    images.extend(list(map(lambda image: \
                  cv2.cvtColor(np.asarray(image),
                  code=cv2.COLOR_GRB2RGB),
                  pdf2image.convert_from_path(document, dpi=dpi))))
    return images

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
    if mess != '':
        st.write(mess)
    image_comparison(img1=before, img2=after,
                             label1='First document',
                             label2='Second document')
    st.image(filled_after, caption='Differance comparison in white')

def mse(img1, img2):
    (h, w, c) = img1.shape
    diff = cv2.subtract(img1, img2)
    err = np.sum(diff ** 2)
    error = err / float(h * w)
    return (error, diff)

def pdf_prep(images1,images2):
    for (index, image) in enumerate(images1):
        mess = ''
        imag1 = np.array(image)
        imag2 = np.array(images2[index])
        (error, diff) = mse(imag1, imag2)
        if error > 0:
            mess = 'On page: ' + str(index) \
                + ' there was an difference of ' \
                + '{:.1f}'.format(error) + '%'
        img_compare(imag1,imag2)
        

if files1 and files2 and submitted is not None:
    if files1.type == 'application/pdf' and files2.type == 'application/pdf':
        images1 = pdf2image.convert_from_bytes(files1.read())
        images2 = pdf2image.convert_from_bytes(files2.read())
        pdf_prep(images1,images2)
    else:
        images1 = cv2.cvtColor(cv2.imdecode(np.frombuffer(files1.read(), np.uint8), 1) , cv2.COLOR_BGR2RGB)
        images2 = cv2.cvtColor(cv2.imdecode(np.frombuffer(files2.read(), np.uint8), 1) , cv2.COLOR_BGR2RGB)
        img_compare(images1, images2)