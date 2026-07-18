import streamlit as st
import requests
import json
import os
from pypdf import PdfReader
import docx2txt

# --- SECURITY UPDATE: Environment Variable Handling ---
# Agar environment variable set nahi hai, toh yeh code locally error dene ke bajaye 
# user ko batayega ke .env file setup karein.
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL")

# Page Layout configuration
st.set_page_config(page_title="Premium AI ATS Platform", page_icon="💼", layout="wide")

# --- HELPER FUNCTIONS ---
def extract_text_from_pdf(file):
    try:
        pdf_reader = PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        return ""

def extract_text_from_docx(file):
    try:
        return docx2txt.process(file)
    except Exception as e:
        return ""

def analyze_resume_via_n8n(resume_text):
    if not N8N_WEBHOOK_URL:
        st.error("❌ Configuration Error: N8N_WEBHOOK_URL not set in environment.")
        return None
        
    payload = {"resume": resume_text}
    try:
        with st.spinner("🔄 Processing via Secure n8n Pipeline..."):
            response = requests.post(N8N_WEBHOOK_URL, json=payload)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception:
        return None

# --- UI INTERFACE ---
st.title("💼 Enterprise AI ATS Resume Suite")
app_mode = st.sidebar.radio("🎯 Select Workspace Action:", ["📄 Upload CV File", "📝 Paste Raw Text", "🏗️ Build CV From Scratch"])

resume_text_to_process = ""

# [REMAINING UI LOGIC REMAINS SAME AS PREVIOUS CODE...]
# (Upar wala sara UI aur logic yahan waise hi rahe ga jaisa pehle tha)
# Sirf security update ensure karne ke liye N8N_WEBHOOK_URL upar define kar diya hai.