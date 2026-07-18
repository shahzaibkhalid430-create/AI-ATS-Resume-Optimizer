import streamlit as st
import json
from groq import Groq

# Page configuration
st.set_page_config(page_title="CV-Forge ATS & Europass Optimizer", page_icon="📝", layout="wide")

# Client initialize
client = Groq(api_key="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")

# Prompts
ATS_SYSTEM_PROMPT = """
You are the core AI engine of an advanced ATS Resume Optimization SaaS. 
Analyze the provided resume text against strict ATS guidelines and provide a highly detailed professional optimization report.
You MUST return your response ONLY as a raw JSON object. Do not include markdown formatting like ```json.

The JSON structure must exactly match this template:
{
  "ats_score": 85,
  "critical_formatting_issues": ["Issue 1", "Issue 2"],
  "keyword_gaps": ["Keyword 1", "Keyword 2"],
  "content_improvements": ["Suggestion 1", "Suggestion 2"],
  "fully_optimized_resume_text": {
    "personal_info": "Name, Contact",
    "professional_summary": "Optimized summary...",
    "work_experience": ["Job Bullet 1", "Job Bullet 2"],
    "education": ["Degree"],
    "skills": ["Skill 1"]
  }
}
"""

EUROPASS_SYSTEM_PROMPT = """
You are a professional resume writer specializing in European Union standards.
Convert the provided resume data exactly into the official Europass CV structure.
You MUST return your response ONLY as a raw JSON object. Do not include markdown formatting.

The JSON structure must exactly match this template:
{
  "format_type": "Official Europass Standard",
  "personal_information": {
    "full_name": "Name",
    "contact_details": "Email, Phone, Address",
    "nationality_or_links": "LinkedIn or Nationality"
  },
  "work_experience": [
    "Position Title - Employer, City, Country (Dates) | Main activities and responsibilities styled for Europass"
  ],
  "education_and_training": [
    "Title of qualification awarded - Organisation, City, Country (Dates)"
  ],
  "language_skills": {
    "mother_tongue": "Urdu/Punjabi/English",
    "other_languages": ["Language - Listening (B2), Reading (C1)"]
  },
  "digital_skills": ["Skill 1"],
  "communication_and_organizational_skills": "Europass style description"
}
"""

st.title("📝 CV-Forge: ATS Checker & Europass Builder")
st.subheader("Apni CV ko ATS-friendly banayein ya Europass format me convert karein")
st.markdown("---")

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 📥 Input Panel")
    resume_input = st.text_area("Yahan apni CV ka saara text copy-paste maren:", height=350)
    
    mode = st.selectbox(
        "✨ Aap kya tayar karna chahte hain?",
        ["ATS Check & Optimize Report", "Official Europass Format CV"]
    )
    
    submit_button = st.button("🚀 Process Karein", type="primary")

with col2:
    st.markdown("### 📊 Live AI Output")
    
    if submit_button and resume_input.strip():
        with st.spinner("AI processing chal rahi hai... Please wait..."):
            try:
                selected_prompt = ATS_SYSTEM_PROMPT if mode == "ATS Check & Optimize Report" else EUROPASS_SYSTEM_PROMPT
                
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": selected_prompt},
                        {"role": "user", "content": f"Process this resume text:\n\n{resume_input}"}
                    ],
                    temperature=0.1,
                    response_format={"type": "json_object"}
                )
                
                data = json.loads(response.choices[0].message.content)
                
                # Create a string representation for download
                download_text = ""
                
                if mode == "ATS Check & Optimize Report":
                    score = data.get("ats_score", 0)
                    st.success(f"## ATS Score: {score}/100")
                    
                    st.markdown("#### ⚠️ Critical Formatting Issues")
                    for issue in data.get("critical_formatting_issues", []):
                        st.write(f"- {issue}")
                        
                    st.markdown("#### 🔍 Missing Keywords")
                    st.write(", ".join(data.get("keyword_gaps", [])))
                    
                    opt = data.get("fully_optimized_resume_text", {})
                    with st.expander("✨ Fully Optimized Text Dekhein"):
                        st.json(opt)
                    
                    # Prepare Download Content
                    download_text = f"ATS SCORE: {score}\n\nOPTIMIZED TEXT:\n{json.dumps(opt, indent=2)}"
                        
                else:
                    st.success(f"## 🇪🇺 {data.get('format_type')}")
                    personal = data.get("personal_information", {})
                    st.markdown(f"### 👤 Personal Details")
                    st.write(f"**Name:** {personal.get('full_name')}")
                    st.write(f"**Contact:** {personal.get('contact_details')}")
                    
                    st.markdown("### 💼 Work Experience")
                    for job in data.get("work_experience", []):
                        st.info(job)
                        
                    # Prepare Download Content
                    download_text = f"EUROPASS CV\n\nName: {personal.get('full_name')}\nContact: {personal.get('contact_details')}\n\nEXPERIENCE:\n" + "\n".join(data.get("work_experience", []))
                
                # --- DOWNLOAD BUTTON INTERFACE ---
                st.markdown("---")
                st.markdown("#### 💾 Output Save Karein")
                st.download_button(
                    label="📥 Download Text File (.txt)",
                    data=download_text,
                    file_name="cv_forge_output.txt",
                    mime="text/plain"
                )
                        
            except Exception as e:
                st.error(f"Error: {e}")
    elif submit_button:
        st.info("Meharbani kar ke pehle CV ka text enter karein!")