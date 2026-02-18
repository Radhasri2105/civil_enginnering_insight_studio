#importing libraries
from dotenv import load_dotenv 
import streamlit as st
import os 
import google.generativeai as genai 
from PIL import Image 

load_dotenv()
my_api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key= my_api_key)

# Function to get gemini response
def get_gemini_response(input_text, image, prompt):
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content([input_text, image[0], prompt])
    return response.text

#function for image processing
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

#prompt for gemini model
input_prompt = """
You are a civil engineer. Please describe the structure in the image and provide details such as its type,

1. Type of structure - Description
2. Materials used - Description
3. Dimensions - Description
4. Construction methods - Description
"""

#Integrate with Web Framework
def main():
    st.set_page_config(page_title="Civil engineering Insight Studio", page_icon="🏗️")
    st.header("🏗️ Civil Engineering Insight Studio")
    input_text = st.text_input("📝 Input Prompt:", key="input")
    uploaded_file = st.file_uploader("🖼️ Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image.", use_container_width=True)

    submit = st.button("🚀 Describe Structure")

    # If submit button is clicked
    if submit:
        try:
            image_data = input_image_setup(uploaded_file)
            response = get_gemini_response(input_text, image_data, input_prompt)
            st.subheader("📋Description of the Civil Engineering Structure:")
            st.markdown(f'<div class="st-ba">{response}</div>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"⚠️Error: {str(e)}")


if __name__ == "__main__":
    main()