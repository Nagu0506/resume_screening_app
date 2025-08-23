from flask import Flask, render_template, request
import os
import docx
import PyPDF2
import re

app = Flask(__name__)

# Folders for uploads
UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# ---------- Helper Functions ----------
def extract_text_from_file(file_path):
    text = ""
    if file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
    elif file_path.endswith(".docx"):
        doc = docx.Document(file_path)
        text = "\n".join([p.text for p in doc.paragraphs])
    elif file_path.endswith(".pdf"):
        with open(file_path, "rb") as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            for page in reader.pages:
                text += page.extract_text() or ""
    return text

def clean_and_tokenize(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9]", " ", text)
    return set(text.split())

# ---------- Routes ----------
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        resume_file = request.files.get("resume")
        job_description = request.form.get("job_description", "")

        if not resume_file or not job_description:
            return "Please provide both resume and job description", 400

        # Save resume
        resume_path = os.path.join(app.config["UPLOAD_FOLDER"], resume_file.filename)
        resume_file.save(resume_path)

        # Extract text
        resume_text = extract_text_from_file(resume_path)
        resume_words = clean_and_tokenize(resume_text)
        jd_words = clean_and_tokenize(job_description)

        matched_skills = sorted(list(resume_words.intersection(jd_words)))

        # Calculate match percentage
        match_percentage = 0
        if jd_words:
            match_percentage = round(len(matched_skills) / len(jd_words) * 100, 2)

        return render_template(
            "results.html",
            resume_name=resume_file.filename,
            matched_skills=matched_skills,
            match_percentage=match_percentage
        )
    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
