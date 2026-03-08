import streamlit as st
import pdfplumber
import docx
import re

# -----------------------------
# Resume text extraction
# -----------------------------

def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:             #  pdfplumber (for reading PDF files)
        for page in pdf.pages:
            if page.extract_text():
                text += page.extract_text()
    return text


def extract_text_from_docx(file):                 ## python-docx (for reading Word files)
    doc = docx.Document(file)
    text = ""
    for para in doc.paragraphs:
        text += para.text
    return text


# -----------------------------
# Clean text
# -----------------------------

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z ]', ' ', text)
    return text


# -----------------------------
# Skill matching
# -----------------------------

required_skills = [
    "python",
    "machine learning",
    "data analysis",
    "sql",
    "pandas",
    "numpy",
    "deep learning"
]


def check_skills(resume_text):

    score = 0

    for skill in required_skills:
        if skill in resume_text:
            score += 1

    return score


# -----------------------------
# Streamlit UI
# -----------------------------

st.title("Resume Shortlisting System")

uploaded_file = st.file_uploader(
    "Upload Resume (PDF or DOCX)", type=["pdf", "docx"]
)

if uploaded_file is not None:

    # Extract text

    if uploaded_file.type == "application/pdf":
        resume_text = extract_text_from_pdf(uploaded_file)

    else:
        resume_text = extract_text_from_docx(uploaded_file)

    cleaned_resume = clean_text(resume_text)

    skill_score = check_skills(cleaned_resume)

    st.subheader("Skill Match Score")
    st.write(skill_score)

    # Simple rule based prediction

    if skill_score >= 3:
        st.success("✅ Resume Shortlisted")

    else:
        st.error("❌ Resume Not Shortlisted")