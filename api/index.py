from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import json
from pathlib import Path

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Lazy-load the data only when needed
def load_student_data():
    data_file = Path(__file__).parent / "q-vercel-python.json"
    if not data_file.exists():
        return []
    with data_file.open() as f:
        return json.load(f)

@app.get("/api")
async def get_marks(name: List[str] = Query(None)):
    """
    Get marks for one or more students by name.
    Example: /api?name=John&name=Alice
    """
    if not name:
        return {"error": "Please provide at least one name"}
    
    students_data = load_student_data()
    marks = []
    for student_name in name:
        mark = next((student["marks"] for student in students_data 
                     if student["name"].lower() == student_name.lower()), None)
        marks.append(mark)
    
    return {"marks": marks}

@app.get("/")
async def root():
    return {"message": "Student Marks API. Use /api?name=X&name=Y to get marks."}
