import os
from pathlib import Path
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key :
    raise ValueError("API key require")

client = Groq(api_key=my_api_key)

model = "llama-3.3-70b-versatile"

try:
    with open("resume.txt", "r", encoding="utf-8") as file:
        candidate_profile = file.read()
except FileNotFoundError:
    candidate_profile = "Profile data missing."

system_prompt = f"""You are the personal AI portfolio assistant for Priyanshu Mohite. 
Your primary job is to act as his representative and answer recruiter questions about his skills, projects, and education.

CRITICAL RULES:
1. Be 100% honest. NEVER make up or hallucinate skills, projects, or experiences.
2. Answer based ONLY on the Candidate Profile provided below. 
3. If a recruiter asks something not mentioned in the profile, politely state that you do not have that information.
4. Keep answers professional and concise.

CANDIDATE PROFILE:
{candidate_profile}
"""