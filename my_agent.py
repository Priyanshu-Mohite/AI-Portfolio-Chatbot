import os
from groq import Groq
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key :
    raise ValueError("API key require")

client = Groq(api_key=my_api_key)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Ye frontend ke port (5173) ki requests ko allow karega
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

class chat_with_ai(BaseModel):
    user_input: str

chat_history = []

@app.post("/chat")
async def chat_with_ai_endpoint(req: chat_with_ai):

    global chat_history

    messages_to_send = [{"role": "system", "content": system_prompt}]
    messages_to_send.extend(chat_history)
    messages_to_send.append({"role": "user", "content": req.user_input})

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages_to_send
    )
    
    ai_reply = response.choices[0].message.content
    
    # 5. Ab conversation history update karenge taaki next time API ko yeh yaad rahe
    chat_history.append({"role": "user", "content": req.user_input})
    chat_history.append({"role": "assistant", "content": ai_reply})
    
    return {"reply": ai_reply}


class jd_request(BaseModel):
    job_description: str

@app.post("/jd-match")
def match_jd(req: jd_request):

    match_prompt = f"""
    Act as an expert IT recruiter. You need to evaluate Priyanshu Mohite's profile against the given Job Description.
    
    Candidate Profile:
    {candidate_profile}
    
    Job Description:
    {req.job_description}
    
    Task:
    1. Compare the candidate's skills, technologies, and projects with the JD requirements.
    2. Give an estimated "Match Percentage" (e.g., 85%).
    3. Provide a brief analysis of what matches perfectly and what skills might be missing.
    Keep the output professional, honest, and concise.
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": match_prompt}]
    )

    return {"match-result": response.choices[0].message.content}