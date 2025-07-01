import streamlit as st
import pandas as pd
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure the API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

st.set_page_config(page_title="AI Question Generator by Shiv", layout="centered")

# Navigation
page = st.radio("Choose a Page", ["Question Generator", "Solution Generator"])

# ------------------------ PAGE 1: Question Generator ------------------------ #
if page == "Question Generator":
    st.title("AI Question Maker By SHIV BHARDWAJ")
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
Ensure all options are relevant, and include detailed solution after questions. 
Follow this instruction: {instruction}. Questions must be original (no plagiarism)."""

                model = genai.GenerativeModel("gemini-2.0-flash")
                response = model.generate_content(prompt)

                st.subheader("Generated Questions")
                st.write(response.text)

# ------------------------ PAGE 2: Solution Generator ------------------------ #
elif page == "Solution Generator":
    st.title("Answer & Solution Evaluator")
    st.subheader("Submit your MCQs and let AI generate explanations")

    with st.form("solution_form"):
        num_qs = st.number_input("How many questions do you want to evaluate?", min_value=1, max_value=10, step=1)
        questions = []
        for i in range(int(num_qs)):
            st.markdown(f"### Question {i+1}")
            q_text = st.text_area(f"Enter Question {i+1}", key=f"q{i}")
            options = st.text_area(f"Enter Options (comma separated)", key=f"opt{i}")
            correct_ans = st.text_input(f"Enter Correct Answer", key=f"ans{i}")
            questions.append({
                "question": q_text,
                "options": options,
                "answer": correct_ans
            })

        submitted = st.form_submit_button("Generate Solutions")

    if submitted:
        with st.spinner("Generating solutions..."):
            prompt = "Generate detailed explanations for the following questions:\n\n"
            for q in questions:
                prompt += f"""Question: {q['question']}
Options: {q['options']}
Correct Answer: {q['answer']}

"""

            prompt += "\nProvide thorough step-by-step explanations for each answer."

            model = genai.GenerativeModel("gemini-2.0-flash")
            response = model.generate_content(prompt)

            st.subheader("Generated Solutions")
            st.write(response.text)

# Footer
st.markdown("""---  
Created by Shiv Bhardwaj {SRB}""")
