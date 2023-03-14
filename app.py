from PIL import Image
import io
import streamlit as st
from io import BytesIO
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="Image Resizer")

BADGES = """
<a href="https://gitHub.com/" title="Star Repo" target="_blank"><img src="https://img.shields.io/github/stars/lukasmasuch/streamlit-pydantic.svg?logo=github&style=social"></a>
<a href="https://twitter.com/aenish_shrestha" title="Follow on Twitter" target="_blank"><img src="https://img.shields.io/twitter/follow/lukasmasuch.svg?style=social&label=Follow"></a>
"""
st.markdown(BADGES, unsafe_allow_html=True)
st.title("Resize Your Image")
st.markdown("*Images are resized in the multiple of 64 and max width or max height of 1024. [ Check Out My Code ](www.google.com)*")

# Download the fixed image
@st.cache_data
def convert_image(img):
    buf = BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    return byte_im


def resizer(image):
    im = Image.open(image)
    col1.write("Original Image :camera:")
    col1.image(im)

    current_width, current_height = im.size

    max_width = min(current_width // 64 * 64, 1024)
    max_height = min(current_height // 64 * 64, 1024)

    aspect_ratio = current_width / current_height
    max_aspect_ratio = max_width / max_height

    if current_width <= max_width and current_height <= max_height:
        # no resizing necessary
        new_width, new_height = current_width, current_height
    elif aspect_ratio > max_aspect_ratio:
        # resize to max_width and maintain aspect ratio
        new_width = max_width
        new_height = int(new_width / aspect_ratio)
    else:
        # resize to max_height and maintain aspect ratio
        new_height = max_height
        new_width = int(new_height * aspect_ratio)
        
    # resize the image using the resize() method
    im_resized = im.resize((new_width, new_height), Image.ANTIALIAS)

    im_resized.save("resized_image.png","PNG")

    col2.write("Resized Image :wrench:")
    col2.image(im_resized)

    col1.write('Original Image Size ')
    col1.write(im.size)
    col2.write('Resized Image Size ')
    col2.write(im_resized.size)



    st.download_button("Download Resized Image", convert_image(im_resized), "resized.png", "image/png")
    components.iframe("https://aenishshrestha.substack.com/embed",height=500)

col1, col2 = st.columns(2)

my_upload = st.file_uploader("Upload an image :rocket:", type=["png", "jpg", "jpeg"])


if my_upload is not None:
    resizer(my_upload)

else : 
    st.warning("Please Upload Your Image")