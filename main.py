import openai
import streamlit as st
from streamlit_chat import message
from dotenv import load_dotenv
import os
from langchain.embeddings.openai import OpenAIEmbeddings
import openai
import streamlit as st
import os
import requests 
import re

st.title('Drake Bling Bakery 🧙')

# Load environment variables from a .env file (containing OPENAI_API_KEY)
load_dotenv()

# Set the OpenAI API key from the environment variable
openai.api_key = os.environ.get('OPENAI_API_KEY')
IMG_FLIP_USERNAME = os.environ.get('IMG_FLIP_USERNAME')
IMG_FLIP_PASSWORD = os.environ.get('IMG_FLIP_PASSWORD')

print("OMEGALUL" + IMG_FLIP_USERNAME + IMG_FLIP_PASSWORD)
def generate_response(user_input ):
    # Generate a response using OpenAI's ChatCompletion API and the specified prompt
    prompt = 'Return the two options for  Drake Hotline Bling meme about: ' + user_input + ". do not return any explaination, just return the list. only return one list. make it funny."
    completion = openai.ChatCompletion.create(
       # model="gpt-3.5-turbo",
        model="gpt-4",
        messages=[
            {"role": "system", "content": "I am creating a Drake Hotline Bling meme. In this meme, Drake disapproves of the first option and approves of the second option. Please provide two short phrases or words for each option, where the first phrase represents a less desirable approach and the second phrase is the more desirable approach. Format your response as a Python list, like this: [option1, option2]"},
            {"role": "user", "content": prompt},
        ])
    response = completion.choices[0].message.content

    # Use regex to extract two options within a list
    options_regex = re.compile(r'\["(.+?)"\s*,\s*"(.+?)"\]')
    match = options_regex.search(response)

    if match:
        options_list = [match.group(1), match.group(2)]
        print("The extracted options are:", options_list)
        return options_list
    else:
        print("The response does not contain two options separated by a comma within a list.")
        return None
    
input_text = st.text_input("", key="input")

def get_text():
    # Call the generate_response function with the user's input
    response = generate_response(input_text)

    # If the response is not None (contains options), proceed
    if response is not None:
        # Print the response to the console
        print(response)
        # Save the two options as response1 and response2
        response1 = response[0]
        response2 = response[1]

        # Set the Imgflip API URL for creating a meme
        url = "https://api.imgflip.com/caption_image"

        # Create a dictionary containing the required parameters for the Imgflip API
        payload = {
            "template_id": "181913649",
            "username": IMG_FLIP_USERNAME,
            "password": IMG_FLIP_PASSWORD,
            "text0": response1,
            "text1": response2,
            "font": "impact",
            "max_font_size": "50"
        }

        # Send a POST request to the Imgflip API with the payload to create the meme
        response = requests.post(url, data=payload)

        # Get the URL of the newly created meme from the API's response
        new_image = response.json()['data']['url']

        # If the user's input is not empty, display the meme using Streamlit
        if input_text:
            st.image(new_image)
        # Return the user's input and the two generated options
        return input_text, [response1, response2]

if st.button("Generate Meme"):
    user_input, generated_options = get_text()  # Capture the generated options

# Initialize the session state for generated responses and past inputs
if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

# If there are generated responses, display the conversation using Streamlit messages
if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])):
        message(st.session_state['past'][i],
                is_user=True, key=str(i) + '_user')
        message(st.session_state["generated"][i], key=str(i))
