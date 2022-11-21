import streamlit as st
from skimage.metrics import structural_similarity
import cv2
import numpy as np

first_image = st.file_uploader("Choose the first file", ['png', 'jpg'], key=1)
second_image = st.file_uploader("Choose the second file", ['png', 'jpg'], key=2)

# Load images
if first_image is not None:
    before = cv2.imdecode(np.frombuffer(first_image.read(), np.uint8), 1)
#    before = cv2.imread(first_image)
if second_image is not None:
    after = cv2.imdecode(np.frombuffer(second_image.read(), np.uint8), 1)

def img_comparison(before, after):
    # Convert images to grayscale
    before_gray = cv2.cvtColor(before, cv2.COLOR_BGR2GRAY)
    after_gray = cv2.cvtColor(after, cv2.COLOR_BGR2GRAY)

    # Compute SSIM between the two images
    (score, diff) = structural_similarity(before_gray, after_gray, full=True)
    print("Image Similarity: {:.4f}%".format(score * 100))

    # The diff image contains the actual image differences between the two images
    # and is represented as a floating point data type in the range [0,1] 
    # so we must convert the array to 8-bit unsigned integers in the range
    # [0,255] before we can use it with OpenCV
    diff = (diff * 255).astype("uint8")
    diff_box = cv2.merge([diff, diff, diff])

    # Threshold the difference image, followed by finding contours to
    # obtain the regions of the two input images that differ
    thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]

    mask = np.zeros(before.shape, dtype='uint8')
    filled_after = after.copy()

    for c in contours:
        area = cv2.contourArea(c)
        if area > 40:
            x,y,w,h = cv2.boundingRect(c)
            cv2.rectangle(before, (x, y), (x + w, y + h), (36,255,12), 2)
            cv2.rectangle(after, (x, y), (x + w, y + h), (36,255,12), 2)
            cv2.rectangle(diff_box, (x, y), (x + w, y + h), (36,255,12), 2)
            cv2.drawContours(mask, [c], 0, (255,255,255), -1)
            cv2.drawContours(filled_after, [c], 0, (0,255,0), -1)

    st.image(before, caption='before')
    st.image(after, caption='after')
    st.image(filled_after, caption='Colored Difference')

if st.button('Compare files'):
    st.write('comparing files')
    img_comparison(before, after)
else:
    st.write('No files compared')