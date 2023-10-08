import streamlit as st

from googletrans import Translator
import easyocr
from gtts import gTTS
from IPython.display import Audio

from langdetect import detect

import PIL
from PIL import ImageDraw





im=PIL.Image.open("C:/Users/Venkata/Downloads/downloadkrish.jpeg")


reader=easyocr.Reader(['hi'])
translator=Translator()

bounds=reader.readtext('C:/Users/Venkata/Downloads/downloadkrish.jpeg',
                       add_margin=0.55,width_ths=0.7,link_threshold=0.8,
                       decoder='beamsearch',blocklist='=.')

def draw_boxes(image,bounds,color='orange',width=2):
  draw=ImageDraw.Draw(image)
  for bound in bounds:
    p0,p1,p2,p3=bound[0]
    draw.line([*p0,*p1,*p2,*p3,*p0],fill=color,width=width)
  return image
image = draw_boxes(im,bounds)
#st.write(image)


text_list=reader.readtext('C:/Users/Venkata/Downloads/downloadkrish.jpeg',
                          add_margin=0.5,width_ths=0.7,link_threshold=0.8,
                          decoder='beamsearch',blocklist='=.')

text_comb =' '.join([x[1] for x in text_list])


text_en = translator.translate(text_comb, src='hi')
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
            ta_tts=gTTS(text_en.text)
            ta_tts.save('trans.mp3')
            Audio('trans.mp3',autoplay=True)
            st.audio('trans.mp3')
    
    
else:
    # Print an error message
    st.warning("Translation failed")