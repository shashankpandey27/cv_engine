import json
import google.generativeai as genai

gemini_model = genai.GenerativeModel('gemini-1.5-flash', generation_config={"response_mime_type": "application/json"})

# Function to call the Gemini LLM API
def ask_gemini(prompt):
    response = gemini_model.generate_content(prompt)
    return response.text

ROLES = [
    "Data Scientist", "Data Engineer", "Full Stack Developer",
    "Frontend Developer", "Backend Developer", "GenAI Expert",
    "UI/UX", "Business Intelligence", "ML Engineer", "DevOps", "Project Management"
]
 
def extract_role_scores(cv_text):

    prompt = f"""
    You are a highly critical CV evaluator.
     
    Given the following CV text:
    '''{cv_text}'''
     
    Evaluate and score the candidate (0 to 100) ONLY for roles that are clearly demonstrated with strong evidence of experience or skills. Be extremely selective — assign high scores ONLY if the candidate has significant, clearly stated experience for that role.
     
    Roles to evaluate:
    {', '.join(ROLES)}
     
    Also extract:
    - **Name** — The full name of the candidate (preferably in CAPITAL LETTERS if found in the CV).
    - **Technical Skills** — A concise list of specific technical skills or tools mentioned in the CV (e.g., Python, SQL, Azure, Spark). Keep it under 20 items.
    = **Total Experience** - Total years of profession experience (numeric only e.g , 5.5)
    - **Languages Spoken** - List of Languages spoken by the candidate
    - **Gender**- Gender of the candidate (male or female)
     
    Return output in strict JSON format like:
    {{
      "Name": "JOHN DOE",
      "Technical Skills": ["Python", "Spark", "SQL", "Docker"],
      "Languages": ["Arabic", "English", "French"],
      "Gender":"male",
      "Experience" : 5.5, 
      "Data Scientist": 82,
      "Machine Learning Engineer": 77,
      ...
    }}
     
    Guidelines:
    - Do NOT include roles where there is little or no evidence. Only include roles with score >= 20.
    - Score 80+ ONLY if the candidate shows deep expertise and hands-on experience (not just mention of the skill).
    - Score 50–70 if there is moderate experience (e.g., 1–3 projects or partial involvement).
    - Score below 50 for light mentions or minor experience.
    - Score 20 if it’s barely relevant.
    - Omit any role with score < 20.
    - The "Name" , "Languages" and "Technical Skills" keys are **mandatory**.
     
    Be extremely objective and conservative — avoid inflating scores. Only include roles that the CV truly supports.
    """
    response = ask_gemini(prompt)
    try:
        return json.loads(response)
    except:
        return {}
