from flask import Flask, render_template, request
import pdfplumber
import docx
import re

app = Flask(__name__)

required_skills = ["python","machine learning","sql","pandas","numpy"]

def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            if page.extract_text():
                text += page.extract_text()
    return text

def extract_text_from_docx(file):
    doc = docx.Document(file)
    text = ""
    for para in doc.paragraphs:
        text += para.text
    return text

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z ]',' ',text)
    return text

def check_skills(text):

    score = 0

    for skill in required_skills:
        if skill in text:
            score += 1

    return score


@app.route("/", methods=["GET","POST"])
def index():

    result = ""

    if request.method == "POST":

        file = request.files["resume"]

        if file.filename.endswith(".pdf"):
            text = extract_text_from_pdf(file)

        else:
            text = extract_text_from_docx(file)

        text = clean_text(text)

        score = check_skills(text)

        if score >= 3:
            result = "Resume Shortlisted ✅"

        else:
            result = "Resume Not Shortlisted ❌"

    return render_template("index.html",result=result)


if __name__ == "__main__":
    app.run(debug=True)