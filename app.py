import os
import streamlit as st
from mcq_generator import generate_mcqs, extract_text_from_pdf

option_labels = ["A", "B", "C", "D"]

st.title("MCQ Generator")

num_questions = st.number_input("Enter the number of questions:", min_value=1)

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if st.button("Submit"):
    document_text = ""
    if uploaded_file is not None:
        document_text = extract_text_from_pdf(uploaded_file)
    else:
        st.warning("Please upload a PDF file.")

    if document_text:
        quiz_result = generate_mcqs(document_text, num_questions)

        st.write("### Generated MCQs")
        for i, mcq in enumerate(quiz_result.mcqs):
            st.markdown(f"### Question {i+1}")
            st.markdown(f"{mcq.question}")
            for label, option in zip(option_labels, mcq.options):
                st.markdown(f"- {label}. {option}")
            st.markdown("")
            st.write(f"Correct Answer: {mcq.correct_answer}")
            st.write(f"Explanation: {mcq.explanation}")
            st.markdown("---")