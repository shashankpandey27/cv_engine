import json
import google.generativeai as genai

gemini_model = genai.GenerativeModel('gemini-1.5-flash', generation_config={"response_mime_type": "application/json"})

# Function to call the Gemini LLM API
def ask_gemini(prompt):
    response = gemini_model.generate_content(prompt)
    return response.text

ROLES = [
    "Data Scientist", "Data Engineer", "Full Stack Developer",
    "Frontend Developer", "Backend Developer",
    "UI/UX", "Business Intelligence", "ML Engineer", "DevOps"
]
 
def extract_role_scores(cv_text):
    prompt = f"""
    From this CV text: '''{cv_text}''', score the candidate from 0-100 for the following roles:
 
    {', '.join(ROLES)} 
    Also extract Name of the candidate 
    **Name:** Full name in CAPITAL LETTERS (if available)
    Return JSON like:
    {{
      "Name" : "XYZ",
      "Data Scientist": 85,
      "Data Engineer": 65,
      ...
    }}
    Only include roles that are relevant with a score >= 20.
    """
    response = ask_gemini(prompt)
    try:
        return json.loads(response)
    except:
        return {}
