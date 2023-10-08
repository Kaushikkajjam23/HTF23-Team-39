import streamlit as st
import os
from googletrans import Translator
import easyocr
from gtts import gTTS
from IPython.display import Audio

from langdetect import detect

import PIL
from PIL import ImageDraw

st.header("MultiLanguage HandWirtten Text Recognition")

if not os.path.exists("uploads"):
    os.makedirs("uploads")


st.sidebar.header("User input value")


def user_input_feature():

    # File Upload Widget
    uploaded_file = st.sidebar.file_uploader(
        "Upload a image file", type=["jpeg", "png", "jpg"])

    if uploaded_file:
        # Display the uploaded file's name and size
        st.sidebar.write("Uploaded file:", uploaded_file.name)
        st.sidebar.write("File size:", uploaded_file.size)

        # Save the uploaded file to the "uploads" folder
        with open(os.path.join("uploads", uploaded_file.name), "wb") as f:
            f.write(uploaded_file.read())
        st.sidebar.success("File uploaded successfully!")


def getImage(file_list):

    if file_list:
        st.header("Uploaded Images ")
        for filename in file_list:
            st.write(filename)

    # File viewer
    selected_file = st.selectbox("Select a file to view", file_list)
    if selected_file:
        file_path = os.path.join("uploads", selected_file)
        file_ext = selected_file.split(".")[-1].lower()

        st.write(f"Viewing: {selected_file}")

        # Display based on file type
        st.image(file_path, use_column_width=True)


user_input_feature()
fileList = os.listdir("uploads")
getImage(fileList)

fL = 'bhaskara.png'

im = PIL.Image.open(fL)

option = st.selectbox('How would you like to be contacted?',
                      ('hi', 'ml', 'ta', 'te', 'gu'))
st.write('You selected:', option)

reader = easyocr.Reader([option])
translator = Translator()

bounds = reader.readtext(fL, add_margin=0.55, width_ths=0.7, link_threshold=0.8,
                         decoder='beamsearch', blocklist='=.')


def draw_boxes(image, bounds, color='orange', width=2):
    draw = ImageDraw.Draw(image)
    for bound in bounds:
        p0, p1, p2, p3 = bound[0]
    draw.line([*p0, *p1, *p2, *p3, *p0], fill=color, width=width)
    return image


image = draw_boxes(im, bounds)
st.write(image)


text_list = reader.readtext(fL, add_margin=0.5, width_ths=0.7, link_threshold=0.8,
                            decoder='beamsearch', blocklist='=.')

text_comb = ' '.join([x[1] for x in text_list])


text_en = translator.translate(text_comb, src=option)
with st.form("Input"):
    list = ['audio', 'text']
    queryText = st.selectbox("Select audio or text", list)
    btnResult = st.form_submit_button('Run')

    # Check if the translation was successful
if text_en.text:
    # Get the detected language code
    language_code = text_en.src
    if btnResult:
        if queryText == 'text':
            st.write(text_en.text)
        else:
            ta_tts = gTTS(text_en.text)
            ta_tts.save('trans.mp3')
            Audio('trans.mp3', autoplay=True)
            st.audio('trans.mp3')


else:
    # Print an error message
    st.warning("Translation failed")
