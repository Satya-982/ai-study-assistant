import streamlit as st
from groq import Groq
from dotenv import load_dotenv
from pypdf import PdfReader
import os

# Load environment variables
load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Page config
st.set_page_config(
    page_title="AI Study Assistant for AIML Students",
    layout="centered"
)

# Title
st.title("🎓 AI Study Assistant for AIML Students")
st.write("Ask anything about ML, DL, NLP, Python, or exams.")

# -------------------------
# 🔹 TEXT QUESTION SECTION
# -------------------------
st.subheader("💬 Ask a Question")

user_question = st.text_input("Ask your question:")

if user_question:
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "user",
                    "content": f"Explain clearly for an AIML student:\n{user_question}"
                }
            ]
        )
        st.success(response.choices[0].message.content)
    except Exception as e:
        st.error(f"Error: {e}")

# -------------------------
# 🔹 PDF UPLOAD SECTION
# -------------------------
st.divider()
st.subheader("📄 Upload PDF & Get Summary")

uploaded_file = st.file_uploader(
    "Upload a PDF (notes, syllabus, etc.)",
    type=["pdf"]
)

if uploaded_file:
    try:
        reader = PdfReader(uploaded_file)
        pdf_text = ""

        for page in reader.pages:
            if page.extract_text():
                pdf_text += page.extract_text()

        st.success("PDF uploaded successfully!")

        if st.button("Summarize PDF"):
            with st.spinner("Summarizing..."):
                summary = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {
                            "role": "user",
                            "content": f"Summarize this PDF for an AIML student:\n{pdf_text}"
                        }
                    ]
                )
                st.info(summary.choices[0].message.content)

    except Exception as e:
        st.error(f"PDF Error: {e}")

# Footer
st.divider()
st.caption("🚀 Built with Python, Streamlit & Groq (LLaMA 3.1)")
