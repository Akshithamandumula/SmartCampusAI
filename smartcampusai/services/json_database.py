import json
import os
import bcrypt
from datetime import datetime
from typing import List, Tuple, Dict, Optional

USERS_FILE = os.path.join(os.path.dirname(__file__), "..", "database", "users.json")
HISTORY_FILE = os.path.join(os.path.dirname(__file__), "..", "database", "history.json")

def ensure_file_exists(file_path: str, default_content: dict):
    """Ensures that the JSON database file exists and contains valid JSON."""
    dir_name = os.path.dirname(file_path)
    if dir_name and not os.path.exists(dir_name):
        os.makedirs(dir_name, exist_ok=True)
        
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(default_content, f, indent=2)
        except Exception:
            pass
            
    # Try reading to ensure it's not corrupt
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            json.load(f)
    except (json.JSONDecodeError, IOError):
        # Re-initialize corrupt files
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(default_content, f, indent=2)
        except Exception:
            pass

def load_data(file_path: str, default_content: dict) -> dict:
    """Loads JSON data from file securely."""
    ensure_file_exists(file_path, default_content)
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default_content

def save_data(file_path: str, data: dict) -> bool:
    """Saves data back to JSON database."""
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return True
    except Exception:
        return False

# Password Hashing Functions
def hash_password(password: str) -> str:
    """Hashes a cleartext password with bcrypt."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def check_password(password: str, hashed_pw: str) -> bool:
    """Verifies a cleartext password against a bcrypt hash."""
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hashed_pw.encode('utf-8'))
    except Exception:
        return False

# User Management Functions
def get_all_users() -> List[dict]:
    """Returns a list of all users from the database."""
    data = load_data(USERS_FILE, {"users": []})
    return data.get("users", [])

def register_user(name: str, student_id: str, email: str, password: str) -> Tuple[bool, str]:
    """Registers a new student and sets up modern academic records."""
    email_clean = email.strip().lower()
    users = get_all_users()
    
    # Check for duplicate email
    if any(u.get("email") == email_clean for u in users):
        return False, "An account with this email already exists."
        
    # Check for duplicate Student ID
    if any(u.get("student_id") == student_id.strip() for u in users):
        return False, "An account with this Student ID already exists."

    hashed = hash_password(password)
    
    # Build default rich student profile
    new_user = {
        "name": name.strip(),
        "student_id": student_id.strip(),
        "email": email_clean,
        "password": hashed,
        "department": "Computer Science & Engineering",
        "semester": "5th Semester",
        "avatar_emoji": "👨‍🎓" if "mr" in name.lower() or "boy" in name.lower() else "👩‍🎓",
        "gpa": 3.92,
        "attendance": 92.5,
        "pending_assignments": 3,
        "exams": 2,
        "theme": "light", # light or dark
        "assignments": [
            {"id": 1, "subject": "CS 301 - Artificial Intelligence", "title": "Neural Networks Project", "due_date": "2026-07-20", "status": "Pending"},
            {"id": 2, "subject": "MAT 204 - Linear Algebra", "title": "Eigenvalues Problem Set", "due_date": "2026-07-18", "status": "Pending"},
            {"id": 3, "subject": "CS 302 - Software Engineering", "title": "Sprint 2 Architecture Design", "due_date": "2026-07-22", "status": "Pending"},
            {"id": 4, "subject": "CS 205 - Data Structures", "title": "Balanced Binary Trees Lab", "due_date": "2026-07-10", "status": "Graded", "grade": "A"}
        ],
        "results": [
            {"course_code": "CS 205", "course_name": "Data Structures", "credits": 4, "grade": "A", "marks": 94},
            {"course_code": "MAT 204", "course_name": "Linear Algebra", "credits": 3, "grade": "A-", "marks": 89},
            {"course_code": "CS 302", "course_name": "Software Engineering", "credits": 4, "grade": "B+", "marks": 87},
            {"course_code": "HUM 101", "course_name": "Technical Writing", "credits": 2, "grade": "A", "marks": 96}
        ],
        "timetable": {
            "Monday": [
                {"time": "09:00 AM - 10:30 AM", "subject": "CS 301 - Artificial Intelligence", "room": "Hall C"},
                {"time": "11:00 AM - 12:30 PM", "subject": "MAT 204 - Linear Algebra", "room": "Room 102"}
            ],
            "Tuesday": [
                {"time": "10:00 AM - 11:30 AM", "subject": "CS 302 - Software Engineering", "room": "Lab 4"}
            ],
            "Wednesday": [
                {"time": "09:00 AM - 10:30 AM", "subject": "CS 301 - Artificial Intelligence", "room": "Hall C"},
                {"time": "11:00 AM - 12:30 PM", "subject": "MAT 204 - Linear Algebra", "room": "Room 102"}
            ],
            "Thursday": [
                {"time": "10:00 AM - 11:30 AM", "subject": "CS 302 - Software Engineering", "room": "Lab 4"},
                {"time": "02:00 PM - 03:30 PM", "subject": "HUM 101 - Technical Writing", "room": "Room 201"}
            ],
            "Friday": [
                {"time": "09:00 AM - 12:00 PM", "subject": "CS 205 - Data Structures Lab", "room": "Computer Lab B"}
            ]
        },
        "notifications": [
            {"id": 1, "title": "Welcome to SmartCampusAI", "message": "Explore your personalized student hub.", "time": "Just now", "read": False},
            {"id": 2, "title": "New Assignment Posted", "message": "Neural Networks Project has been posted in CS 301.", "time": "2 hours ago", "read": False},
            {"id": 3, "title": "AI Suggestion", "message": "Based on your progress, we recommend focusing on Neural Networks this week.", "time": "2 days ago", "read": False}
        ],
        "activities": [
            {"time": datetime.now().strftime("%Y-%m-%d %H:%M"), "type": "System", "description": "Account registered successfully."}
        ]
    }
    
    users.append(new_user)
    if save_data(USERS_FILE, {"users": users}):
        return True, "Registration successful! You can now log in."
    return False, "Failed to save user. Please try again."

def authenticate_user(email: str, password: str) -> Optional[dict]:
    """Authenticates user. Returns user dictionary if validated, otherwise None."""
    email_clean = email.strip().lower()
    users = get_all_users()
    for user in users:
        if user.get("email") == email_clean:
            if check_password(password, user.get("password")):
                return user
    return None

def update_user(updated_user_data: dict) -> bool:
    """Updates a user record in the database."""
    email = updated_user_data.get("email")
    if not email:
        return False
        
    data = load_data(USERS_FILE, {"users": []})
    users = data.get("users", [])
    
    updated = False
    for i, user in enumerate(users):
        if user.get("email") == email:
            users[i] = updated_user_data
            updated = True
            break
            
    if updated:
        return save_data(USERS_FILE, {"users": users})
    return False

def delete_user(email: str) -> bool:
    """Deletes a user record by email."""
    data = load_data(USERS_FILE, {"users": []})
    users = data.get("users", [])
    
    initial_len = len(users)
    users = [u for u in users if u.get("email") != email.strip().lower()]
    
    if len(users) < initial_len:
        return save_data(USERS_FILE, {"users": users})
    return False

# Chat History Management
def save_chat_history(email: str, messages: list) -> bool:
    """Saves user's chat history messages in history.json."""
    email_clean = email.strip().lower()
    data = load_data(HISTORY_FILE, {"history": []})
    histories = data.get("history", [])
    
    found = False
    for h in histories:
        if h.get("email") == email_clean:
            h["messages"] = messages
            h["last_updated"] = datetime.now().isoformat()
            found = True
            break
            
    if not found:
        histories.append({
            "email": email_clean,
            "messages": messages,
            "last_updated": datetime.now().isoformat()
        })
        
    data["history"] = histories
    return save_data(HISTORY_FILE, data)

def load_chat_history(email: str) -> list:
    """Loads chat messages for a user from history.json."""
    email_clean = email.strip().lower()
    data = load_data(HISTORY_FILE, {"history": []})
    histories = data.get("history", [])
    
    for h in histories:
        if h.get("email") == email_clean:
            return h.get("messages", [])
    return []
