import streamlit as st
import pandas as pd
import os
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()
# Configure the API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
st.title("AI Question Maker By SHIV BHARDWAJ")
st.subheader("Let me generate some brain storming questions for you")

with st.sidebar:
    st.title("Enter your requirements")
    subject = st.text_input("Enter subject")
    topic = st.text_input("Enter topic")
    sub_topic = st.text_input("Enter sub topic (Comma separated)")
    question = st.slider("Enter the no. of questions required", min_value=1, max_value=10, step=1)
    question_difficulty = st.select_slider("Enter the difficulty level", options=["Very Easy","Easy", "Medium", "Hard", "Very Hard"])
    generate1 = st.button("Generate Questions")


if generate1:
    if not subject or not sub_topic:
        st.warning("Please provide a title and keywords.")

    else:
        with st.spinner("Generating questionss..."):
            prompt = f"""Give me {question} Multiple choice questions of subject {subject} where the required questions is of topic {topic} and the sub topic is {sub_topic}, the difficulty is {question_difficulty}
and with detailed solutions. Also, make sure the questions are original and not plagiarized"""

            model = genai.GenerativeModel("gemini-2.0-flash")
            response = model.generate_content(prompt)

            st.subheader("Generated Blog")
            st.write(response.text)

st.markdown("""Created by Shiv Bhardwaj {SRB}""")

