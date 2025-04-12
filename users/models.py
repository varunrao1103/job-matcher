import os
import re
import nltk
import PyPDF2
import numpy as np
from docx import Document
from django.db import models
from django.conf import settings
from django.core.files.storage import default_storage
from django.contrib.auth.models import AbstractUser
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sentence_transformers import SentenceTransformer

# Download necessary NLTK data
nltk.download("wordnet")
nltk.download("stopwords")
nltk.download("punkt")

# Load the BERT model
bert_model = SentenceTransformer("all-MiniLM-L6-v2")

# Ensure NLTK stopwords are available
try:
    stop_words = set(stopwords.words("english"))
except LookupError:
    nltk.download("stopwords")
    stop_words = set(stopwords.words("english"))

class CustomUser(AbstractUser):
    USER_TYPES = ("recruiter", "Recruiter"), ("job_seeker", "Job Seeker")
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default="job_seeker")
    
    def __str__(self):
        return self.username

class Job(models.Model):
    recruiter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    requirements = models.TextField()
    posted_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    job_seeker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cover_letter = models.TextField()
    resume = models.FileField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    match_percentage = models.FloatField(default=0)  # Store match percentage

    def extract_resume_text(self):
        if not self.resume:
            return "No resume uploaded."

        # Ensure correct path inside media/resumes/
        full_path = default_storage.path(self.resume.name)

        if not os.path.exists(full_path):
            return "File not found."

        text = ""
        try:
            with open(full_path, "rb") as f:
                pdf_reader = PyPDF2.PdfReader(f)
                for page in pdf_reader.pages:
                    text += page.extract_text() or ""  # Extract text from each page
        except Exception as e:
            return f"Error reading PDF: {str(e)}"

        return text.strip() if text.strip() else "No text extracted." 
    
    @staticmethod
    def preprocess_text(text):
        """Lowercase, remove special chars, lemmatize, and remove stopwords."""
        lemmatizer = WordNetLemmatizer()
        text = text.lower()
        text = re.sub(r"[^a-z\s]", "", text)  # Remove special characters
        words = word_tokenize(text)
        words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]
        return " ".join(words)
    
    def calculate_match(self):
        """Calculate match percentage using BERT embeddings."""
        resume_text = self.extract_resume_text()
        if "Error" in resume_text or "No text" in resume_text:
            return 0  # Handle errors
        
        job_text = self.job.description + " " + self.job.requirements
        
        # Preprocess text
        resume_text = self.preprocess_text(resume_text)
        job_text = self.preprocess_text(job_text)
        
        if not resume_text.strip() or not job_text.strip():
            return 0  # Avoid BERT processing empty text
        
        print(resume_text)
        print(job_text)
        
        # Get BERT embeddings
        resume_embedding = bert_model.encode(resume_text)
        job_embedding = bert_model.encode(job_text)
        
        if resume_embedding is None or job_embedding is None:
            return 0
        
        # Compute cosine similarity
        similarity = np.dot(resume_embedding, job_embedding) / (
            np.linalg.norm(resume_embedding) * np.linalg.norm(job_embedding)
        )
        
        return round(similarity * 100, 2)
    
    def save(self, *args, **kwargs):
        """Calculate match percentage before saving"""
        self.match_percentage = self.calculate_match()
        super().save(*args, **kwargs)

