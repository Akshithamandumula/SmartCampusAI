import os
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Retrieve values
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")

# Dynamic OpenAI library version detection for backwards compatibility
HAS_OPENAI_CLIENT = False
HAS_OPENAI_LEGACY = False

try:
    from openai import OpenAI
    HAS_OPENAI_CLIENT = True
except ImportError:
    try:
        import openai
        if hasattr(openai, "ChatCompletion"):
            HAS_OPENAI_LEGACY = True
    except ImportError:
        pass

def is_api_configured() -> bool:
    """Checks if a valid-looking OpenAI API key is configured."""
    key = OPENAI_API_KEY.strip()
    return bool(key and key != "your_api_key_here")

def generate_ai_response(prompt: str, chat_history: list = None, student_info: dict = None) -> str:
    """
    Generates a response using OpenAI if configured.
    Gracefully falls back to an intelligent campus-specific local response engine 
    if not configured or if the installed OpenAI library is outdated.
    """
    if is_api_configured():
        if HAS_OPENAI_CLIENT:
            try:
                client = OpenAI(api_key=OPENAI_API_KEY)
                
                # Format system prompt with user identity if available
                system_prompt = "You are SmartCampusAI, a premium AI academic advisor and helper for college students."
                if student_info:
                    system_prompt += f" You are talking to {student_info.get('name')}, a student in the {student_info.get('department')} department (currently in {student_info.get('semester')}) with CGPA {student_info.get('gpa')}. Keep answers concise, premium, encouraging, and academically helpful."
                
                messages = [{"role": "system", "content": system_prompt}]
                
                # Append context history
                if chat_history:
                    for msg in chat_history[-6:]:
                        messages.append({"role": msg["role"], "content": msg["content"]})
                        
                messages.append({"role": "user", "content": prompt})
                
                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=messages,
                    temperature=0.7,
                    max_tokens=600
                )
                return response.choices[0].message.content
                
            except Exception as e:
                time.sleep(1.5)
                return f"⚠️ **OpenAI API Client Error:** `{str(e)}` \n\n*Falling back to SmartCampusAI local advisor system...*\n\n{get_local_mock_response(prompt, student_info)}"
                
        elif HAS_OPENAI_LEGACY:
            try:
                import openai
                openai.api_key = OPENAI_API_KEY
                
                system_prompt = "You are SmartCampusAI, a premium AI academic advisor and helper for college students."
                if student_info:
                    system_prompt += f" You are talking to {student_info.get('name')}, a student in the {student_info.get('department')} department (currently in {student_info.get('semester')}) with CGPA {student_info.get('gpa')}. Keep answers concise, premium, encouraging, and academically helpful."
                
                messages = [{"role": "system", "content": system_prompt}]
                
                if chat_history:
                    for msg in chat_history[-6:]:
                        messages.append({"role": msg["role"], "content": msg["content"]})
                        
                messages.append({"role": "user", "content": prompt})
                
                response = openai.ChatCompletion.create(
                    model=MODEL_NAME,
                    messages=messages,
                    temperature=0.7,
                    max_tokens=600
                )
                return response['choices'][0]['message']['content']
                
            except Exception as e:
                time.sleep(1.5)
                return f"⚠️ **OpenAI API Legacy Error:** `{str(e)}` \n\n*Falling back to SmartCampusAI local advisor system...*\n\n{get_local_mock_response(prompt, student_info)}"
                
        else:
            time.sleep(1.5)
            warning_prefix = "⚠️ **Outdated OpenAI Library:** \n" \
                             "The installed `openai` library version is too old to support modern ChatCompletion endpoint APIs (requires Python 3.8+ to install OpenAI v1.0.0+).\n\n"
            return warning_prefix + get_local_mock_response(prompt, student_info)
    else:
        # Simulate network latency for a high-quality feel
        time.sleep(1.5)
        return get_local_mock_response(prompt, student_info)

def get_local_mock_response(prompt: str, student_info: dict = None) -> str:
    """
    Intelligent local rule-based response engine.
    Ensures application utility even in offline/mock mode.
    """
    p = prompt.lower()
    student_name = student_info.get("name", "Student") if student_info else "Student"
    dept = student_info.get("department", "Engineering") if student_info else "Engineering"
    gpa = student_info.get("gpa", 3.92) if student_info else 3.92
    
    header = "🤖 **[SmartCampusAI Local Advisor]**\n\n"
    
    if "hello" in p or "hi " in p or "hey" in p:
        return f"{header}Hello {student_name}! I'm your SmartCampusAI Local Advisor. How can I help you today? You can ask me about your grades, assignments, exam preparation, timetable, or career advice!"
        
    elif "grade" in p or "cgpa" in p or "gpa" in p or "result" in p:
        return f"{header}Sure! Currently, you have an outstanding CGPA of **{gpa}** in the **{dept}** program. Your highest score is in Technical Writing and Data Structures. Keep up the amazing work!"
        
    elif "assignment" in p or "homework" in p or "due" in p:
        return f"{header}You have **3 pending assignments**:\n" \
               f"1. **Neural Networks Project** (CS 301) — due July 20 (High Priority)\n" \
               f"2. **Eigenvalues Problem Set** (MAT 204) — due July 18\n" \
               f"3. **Sprint 2 Architecture Design** (CS 302) — due July 22\n\n" \
               f"Let me know if you need help with any specific topic!"
               
    elif "timetable" in p or "class" in p or "schedule" in p:
        return f"{header}Here is your core schedule:\n" \
               f"- **Mon/Wed**: AI (09:00 AM) & Linear Algebra (11:00 AM)\n" \
               f"- **Tue/Thu**: Software Engineering (10:00 AM)\n" \
               f"- **Friday**: Data Structures Lab (09:00 AM)\n\n" \
               f"All rooms are listed on the Timetable tab."
               
    elif "exam" in p or "test" in p or "study" in p or "preparation" in p:
        return f"{header}To prepare for your upcoming exams in Linear Algebra and Software Engineering:\n" \
               f"1. **Focus on key weights**: Review midterm questions and programming labs.\n" \
               f"2. **Ask me specific questions**: Try asking me 'Explain Eigenvalues' or 'What is Agile design pattern?'\n" \
               f"3. **Mock tests**: Practice balancing binary trees and neural network feedforward calculations."
               
    elif "career" in p or "job" in p or "resume" in p or "internship" in p:
        return f"{header}Since you are studying **{dept}** with a strong GPA of **{gpa}**, here are top recommendations:\n" \
               f"- **Roles**: Aim for Software Development Engineer (SDE) or AI Engineer internships.\n" \
               f"- **Skills**: Deepen your python capabilities, practice DSA, and build 2-3 custom LLM integrations (like this application!).\n" \
               f"- **Recommendation**: Create a GitHub repository for your projects and showcase them on LinkedIn."
               
    elif "python" in p or "code" in p or "programming" in p:
        return f"{header}I love coding! If you're building software in Python:\n" \
               f"- Make sure to use virtual environments (`venv`).\n" \
               f"- Keep environment secrets in `.env` files using `python-dotenv`.\n" \
               f"- Write modular, clean code, handling key errors with `try-except` blocks."
               
    else:
        return f"{header}That is an interesting question! Since I'm currently running in Local Advisor mode (no OpenAI API key detected in `.env`), my answers are rule-based.\n\n" \
               f"To experience full conversational AI power, please update the **`OPENAI_API_KEY`** variable in your `.env` file in the project directory!"
