import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from PIL import Image
import google.generativeai as genai

# Load API Key
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Page Setup
st.set_page_config(page_title="AI Question Generator by Shiv", layout="centered")
page = st.radio("Choose a Page", ["Question Generator", "Solution Generator"])

# ------------------------ PAGE 1: Question Generator ------------------------ #
if page == "Question Generator":
    st.title("AI Question Maker By SHIVAM BHARDWAJ")
    st.subheader("Let me generate some brain storming questions for you")

    with st.sidebar:
        st.title("Enter your requirements")
        subject = st.text_input("Enter subject")
        topic = st.text_input("Enter topic")
        sub_topic = st.text_input("Enter sub topic (Comma separated)")
        question = st.slider("Enter the no. of questions required", min_value=1, max_value=10, step=1)
        question_difficulty = st.select_slider("Enter the difficulty level",
                                               options=["Very Easy", "Easy", "Medium", "Hard", "Very Hard"])
        instruction = st.text_input("Enter instruction")
        generate1 = st.button("Generate Questions")

    if generate1:
        if not subject or not sub_topic:
            st.warning("Please provide subject and sub-topic.")
        else:
            with st.spinner("Generating questions..."):
                prompt = f"""Give me {question} Multiple Choice Questions (MCQs) for the subject "{subject}", 
of topic "{topic}" and sub-topics: {sub_topic}. Difficulty level: {question_difficulty}. 
Ensure all options are relevant, and include detailed solution after each and every question. 
Follow this instruction: {instruction}. Questions must be original (no plagiarism)."""

                model = genai.GenerativeModel("gemini-2.0-flash")
                response = model.generate_content(prompt)

                st.subheader("Generated Questions")
                st.write(response.text)

# ------------------------ PAGE 2: Updated Solution Generator ------------------------ #
elif page == "Solution Generator":
    st.title("📚 Answer & Solution Evaluator")
    st.subheader("Submit questions manually or via image (supports equations too)")

    reload_btn = st.button("🔄 Reload Form")

    if reload_btn:
        st.session_state.clear()
        st.experimental_rerun()

    with st.form("solution_form"):
        q_text = st.text_area("✍️ Enter your Question (can include equations)")
        uploaded_image = st.file_uploader("🖼️ Or Upload an Image of the Question", type=["jpg", "jpeg", "png"])

        submitted = st.form_submit_button("Generate Solutions")

    if submitted:
        model = genai.GenerativeModel("gemini-2.0-flash")

        with st.spinner("Processing your question and generating a solution..."):

            parts = []
            prompt = """You are a subject matter expert. Solve the following question and provide a detailed step-by-step explanation. 
If it's a math or equation-based question, include formulas and logic used.\n\n"""

            if q_text:
                parts.append(prompt + q_text)

            if uploaded_image:
                image = Image.open(uploaded_image)
                parts = [prompt, image]  # use image+text input (multimodal)

            try:
                response = model.generate_content(parts)
                st.subheader(" AI-Generated Solution")
                st.write(response.text)
            except Exception as e:
                st.error(f"Error: {e}")

# Footer
st.markdown("""---  
Created by **Shivam Bhardwaj** {SRB}""")

