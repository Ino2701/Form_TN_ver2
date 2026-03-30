from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import random

app = FastAPI()

# ===== CORS =====
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== USERS =====
users = [
    {"username": "admin", "password": "123", "role": "admin"},
    {"username": "user", "password": "123", "role": "user"}
]

# ===== QUESTIONS =====
questions = [
    {
        "id": 1,
        "question": "React là thư viện của ngôn ngữ nào?",
        "options": ["Python", "JavaScript", "Java", "C#"],
        "correct_answer": "JavaScript"
    },
    {
        "id": 2,
        "question": "HTML là gì?",
        "options": ["Ngôn ngữ lập trình", "Ngôn ngữ đánh dấu", "CSDL", "API"],
        "correct_answer": "Ngôn ngữ đánh dấu"
    },
    {
        "id": 3,
        "question": "CSS dùng để làm gì?",
        "options": ["Logic", "DB", "UI", "API"],
        "correct_answer": "UI"
    },
    {
        "id": 4,
        "question": "Python là gì?",
        "options": ["Compiled", "Interpreted", "ASM", "Machine"],
        "correct_answer": "Interpreted"
    },
    {
        "id": 5,
        "question": "HTTP là gì?",
        "options": ["HTTP", "FTP", "SMTP", "TCP"],
        "correct_answer": "HTTP"
    }
]

scores = []

# ===== MODELS =====
class LoginRequest(BaseModel):
    username: str
    password: str

class Answer(BaseModel):
    question_id: int
    selected_answer: str

class SubmitRequest(BaseModel):
    username: str
    answers: List[Answer]

class QuestionCreate(BaseModel):
    question: str
    options: List[str]
    correct_answer: str


# ===== LOGIN =====
@app.post("/login")
def login(data: LoginRequest):
    user = next((u for u in users if u["username"] == data.username and u["password"] == data.password), None)
    if not user:
        return {"error": "Sai tài khoản"}
    return {"role": user["role"], "username": user["username"]}


# ===== QUESTIONS =====
@app.get("/questions")
def get_questions():
    num = random.randint(5, min(10, len(questions)))
    selected = random.sample(questions, num)

    return [
        {
            "id": q["id"],
            "question": q["question"],
            "options": q["options"]
        }
        for q in selected
    ]


# ===== SUBMIT =====
@app.post("/submit")
def submit(data: SubmitRequest):
    score = 0
    results = []

    for ans in data.answers:
        q = next((q for q in questions if q["id"] == ans.question_id), None)

        if not q:
            continue

        is_correct = ans.selected_answer == q["correct_answer"]

        if is_correct:
            score += 1

        results.append({
            "question_id": q["id"],
            "selected_answer": ans.selected_answer,
            "correct_answer": q["correct_answer"],
            "is_correct": is_correct
        })

    scores.append({
        "username": data.username,
        "score": score,
        "total": len(results)
    })

    return {
        "total": len(results),
        "score": score,
        "details": results
    }


# ===== ADMIN =====
@app.post("/add-question")
def add_question(q: QuestionCreate):
    new_id = max([q["id"] for q in questions]) + 1 if questions else 1
    questions.append({
        "id": new_id,
        "question": q.question,
        "options": q.options,
        "correct_answer": q.correct_answer
    })
    return {"message": "Đã thêm"}


@app.get("/scores")
def get_scores():
    return scores