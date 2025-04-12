 # How to Run the Job Matcher Project (windows):
   1. git clone https://github.com/your-username/job-matcher.git
   2. cd job-matcher
   3. python -m venv venv 
   4. venv\Scripts\activate
   5. pip install -r requirements.txt
   6. python manage.py migrate
   7. python manage.py runserver
   8. acccess the portal - http://127.0.0.1:8000/

# Job Matcher - Django & NLP Based Job Portal

A smart job portal built with Django where **recruiters can post jobs** and **job seekers can apply** using their resumes.
The platform leverages **NLP techniques and BERT embeddings** to compute how well a candidate's resume matches the job description —
providing a **match percentage** for each application.

---


## 🚀 Features

### 👤 User Authentication
- Custom user model with roles: **Recruiter** and **Job Seeker**
- Sign up, log in, log out
- Role-based dashboard redirection

### 💼 Recruiter Dashboard
- Post and manage jobs
- View all applications with match percentage scores

### 🧑‍💻 Job Seeker Dashboard
- Search and filter jobs
- View job details
- Apply to jobs by uploading resumes (PDF support)
- Prevents duplicate applications

### 🧠 Intelligent Resume Matching
- Uses **BERT model** (`all-MiniLM-L6-v2`) to semantically compare resume text and job description
- Preprocessing includes **lemmatization, tokenization**, and **stopword removal** via **NLTK**
- Parses resumes from **PDFs** (DOCX support planned)

---

## 🛠️ Tech Stack

- **Backend**: Django
- **Database**: SQLite (default)
- **Authentication**: Django’s built-in system
- **Text Processing**: NLTK
- **Similarity Matching**: SentenceTransformers (BERT)
- **Resume Parsing**: PyPDF2 (PDF)

---

