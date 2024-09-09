import numpy as np
import pickle
import streamlit as st
import warnings
import base64

warnings.filterwarnings('ignore')

# Load the model
loaded_model = pickle.load(open("personality_model.sav", 'rb'))

# Function to add background from a local file
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded_image}");
            background-attachment: fixed;
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Use your local image file path
add_bg_from_local("rat.jpg")

# Prediction function
def personality_prediction(input_data):
    try:
        input_data_np = np.asarray(input_data, dtype=np.float32).reshape(1, -1)
        prediction = loaded_model.predict(input_data_np)[0]
        
        # Mapping numbers to personality traits with font styling
        personality_map = {
            3: "𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐢𝐛𝐥𝐞",
            1: "𝐄𝐱𝐭𝐫𝐚𝐯𝐞𝐫𝐭𝐞𝐝",
            4: "𝐒𝐞𝐫𝐢𝐨𝐮𝐬",
            0: "𝐃𝐞𝐩𝐞𝐧𝐝𝐚𝐛𝐥𝐞",
            2: "𝐋𝐢𝐯𝐞𝐥𝐲"
        }
        
        # Return the corresponding personality trait with a message
        return f'<span style="font-size:20px; color:black;">𝐓𝐡𝐞 𝐏𝐫𝐞𝐝𝐢𝐜𝐭𝐞𝐝 𝐑𝐞𝐬𝐮𝐥𝐭 𝐟𝐨𝐫 𝐭𝐡𝐞 𝐠𝐢𝐯𝐞𝐧 𝐯𝐚𝐥𝐮𝐞𝐬 𝐢𝐬 : {personality_map.get(prediction, "Unknown Personality")}</span>'
    
    except Exception as e:
        return f"Error in prediction: {e}"

def main():
    st.title('𝐏𝐞𝐫𝐬𝐨𝐧𝐚𝐥𝐢𝐭𝐲 𝐏𝐫𝐞𝐝𝐢𝐜𝐭𝐢𝐨𝐧')

    # Input fields
    gender = st.selectbox('𝐆𝐞𝐧𝐝𝐞𝐫', ['Male', 'Female'])
    age = st.text_input('𝐀𝐠𝐞')
    openness = st.text_input('𝐎𝐩𝐞𝐧𝐧𝐞𝐬𝐬')
    neuroticism = st.text_input('𝐍𝐞𝐮𝐫𝐨𝐭𝐢𝐜𝐢𝐬𝐦')
    conscientiousness = st.text_input('𝐂𝐨𝐧𝐬𝐜𝐢𝐞𝐧𝐭𝐢𝐨𝐮𝐬𝐧𝐞𝐬𝐬')
    agreeableness = st.text_input('𝐀𝐠𝐫𝐞𝐞𝐚𝐛𝐥𝐞𝐧𝐞𝐬𝐬')
    extraversion = st.text_input('𝐄𝐱𝐭𝐫𝐚𝐯𝐞𝐫𝐬𝐢𝐨𝐧')

    # Convert gender to numeric
    gender = 0 if gender == 'Male' else 1

    # Validate inputs and convert them to floats
    try:
        input_data = [
            gender,
            float(age),
            float(openness),
            float(neuroticism),
            float(conscientiousness),
            float(agreeableness),
            float(extraversion)
        ]
        input_valid = True
    except ValueError:
        st.error("Please enter valid numeric values for all input fields.")
        input_valid = False
    
    # Prediction code
    if input_valid and st.button('𝐏𝐑𝐄𝐃𝐈𝐂𝐓'):
        prediction_result = personality_prediction(input_data)
        st.markdown(prediction_result, unsafe_allow_html=True)

if __name__ == '__main__':
    main()
