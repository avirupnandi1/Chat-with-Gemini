
import streamlit as st 
import google.generativeai as genai 
import google.ai.generativelanguage as glm 
from dotenv import load_dotenv
from PIL import Image
import os 
import io 
import json 
import requests 
from streamlit_lottie import st_lottie

load_dotenv()

def image_to_byte_array(image: Image) -> bytes:
    imgByteArr = io.BytesIO()
    image.save(imgByteArr, format=image.format)
    imgByteArr=imgByteArr.getvalue()
    return imgByteArr

API_KEY = os.environ.get("GOOGLE_API_KEY")
genai.configure(api_key=API_KEY)


# Set the width of the page
st.set_page_config(layout="centered")

#st.write("![Your Awsome GIF](https://www.aalpha.net/wp-content/uploads/2020/11/ChatBot_ace-1.gif)")

st.markdown(
    """
    <style>
        h1 {
            text-align: center;
            color: red;
            font-family: 'Julee', cursive;
        }
    </style>
    """,
    unsafe_allow_html=True,
)
# Set the header in the middle of the page with a larger size
st.markdown("<h1 style='text-align: center; color: red;'>Gemini is here!🤖</h1>", unsafe_allow_html=True)



gemini_pro, gemini_vision = st.tabs(["Gemini Pro", "Gemini Pro Vision"])

def main():
    with gemini_pro:
        
        st.header("Dive into the Gemini Pro ")
        st.write("")

        prompt = st.text_input("Go Ahead with Your Question", placeholder="Ask here", label_visibility="visible")
        model = genai.GenerativeModel("gemini-pro")

        if st.button("SEND"):
            response = model.generate_content(prompt)

            st.write("")
        
            st.write("")

            st.markdown(response.text)

    with gemini_vision:
        st.header("Dive into the Gemini Pro Vision")
        st.write("")

        image_prompt = st.text_input("Interact with the Image", placeholder="Ask here", label_visibility="visible")
        
        uploaded_file = st.file_uploader("Choose an Image", accept_multiple_files=False, type=["png", "jpg", "jpeg", "img", "webp"])

        if uploaded_file is not None:
            st.image(Image.open(uploaded_file), use_column_width=True)

            st.markdown("""
                <style>
                        img {
                            border-radius: 10px;
                        }
                </style>
                """, unsafe_allow_html=True)
            
        if st.button("GET RESPONSE", use_container_width=True):
            model = genai.GenerativeModel("gemini-pro-vision")

            if uploaded_file is not None:
                if image_prompt != "":
                    image = Image.open(uploaded_file)

                    response = model.generate_content(
                        glm.Content(
                            parts = [
                                glm.Part(text=image_prompt),
                                glm.Part(
                                    inline_data=glm.Blob(
                                        mime_type="image/jpeg",
                                        data=image_to_byte_array(image)
                                    )
                                )
                            ]
                        )
                    )

                    response.resolve()

                    st.write("")
                    st.write(":blue[Response]")
                    st.write("")

                    st.markdown(response.text)

                else:
                    st.write("")
                    st.header(":red[Please Provide a prompt]")

            else:
                st.write("")
                st.header(":red[Please Provide an image]")

if __name__ == "__main__":
    main()