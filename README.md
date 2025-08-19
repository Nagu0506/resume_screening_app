Resume Screening App:

A simple Flask web application that helps HR/recruiters check how well a candidate's resume matches a given job description.  
The app supports .pdf, .docx, and .txt resumes.

---

Features:
- Upload a resume (.pdf, .docx, .txt)
- Enter a job description
- Extracts and cleans text from resume
- Matches resume with job description
- Shows **matched skills** and **percentage match**

Project Structure:
resume_screening_app/
│── app.py
│── templates/
│ ├── index.html
│ ├── results.html
│── static/
│── uploads/
│── README.md
│── requirements.txt

Usage:
Install required dependencies:
pip install -r requirements.txt

Run the app:
python app.py

Open browser and go to:
http://127.0.0.1:5000/

Upload a resume and enter a job description.
The app will display matched skills and match percentage.