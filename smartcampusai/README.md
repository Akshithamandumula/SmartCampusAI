# SmartCampusAI 🎓

SmartCampusAI is a premium, production-ready student dashboard web application built with **Python** and **Streamlit**. It integrates secure user authorization, student records tracking, interactive assignment lists, and an AI-driven academic assistant.

The user interface features a custom-designed modern **Glassmorphism** layout with soft shadows, responsive typography, and full dark-mode synchronization.

---

## 🚀 Key Features

* **Secure Authentication**: Multi-page session authorization using hashed credentials (`bcrypt`) saved in a lightweight JSON database.
* **Modern UI Layout**: Visual card grids, progress bars, and custom styled tables using custom CSS templates in `styles/style.css`.
* **AI Academic Advisor**: Chatbot integration utilizing the OpenAI completions API. Includes automatic mock fallback when offline or when no API key is specified.
* **Academic Dashboard**:
  - *Attendance Tracker*: Lectures attended rate with visual compliance progress bars.
  - *Assignments Board*: Due dates list and interactive submission forms.
  - *Grades Records*: Cumulative CGPA calculations and course results tables.
  - *Timetable Viewer*: Weekly classes schedules.
  - *Notification Center*: Alert updates with "Mark all read" states.
* **Display Preferences**: Interactive dark/light mode toggle with state persistence across sessions.

---

## 📂 Project Structure

```text
SmartCampusAI/
│
├── .streamlit/
│   └── config.toml          # Custom Streamlit layout and default page configuration
│
├── assets/
│   ├── logo.png             # Application logo (Generated)
│   └── background.jpg       # Campus background illustration (Generated)
│
├── database/
│   ├── users.json           # User profiles database (Hashed Passwords, Profile Stats)
│   └── history.json         # AI Chat history logs per student
│
├── components/
│   ├── auth.py              # Page access controls and session helpers
│   ├── cards.py             # Glassmorphism metric cards rendering wrappers
│   ├── navbar.py            # Dashboard top headers and theme toggles
│   └── sidebar.py           # Option-menu custom sidebar navigation
│
├── pages/
│   ├── Dashboard.py         # Primary workspace router page
│   ├── Login.py             # Login credentials page
│   ├── Profile.py           # Personal details management
│   ├── Register.py          # Student signup page
│   └── Settings.py          # System preference options & password updater
│
├── services/
│   ├── ai_service.py        # OpenAI API query broker and local advisor rules fallback
│   └── json_database.py     # Users & history records manager
│
├── styles/
│   └── style.css            # Custom CSS definitions (Transitions, typing animation)
│
├── utils/
│   ├── helpers.py           # Style injection and config initialization
│   └── validation.py        # Input formats validation helpers
│
├── .env                     # Local environment file (API Keys)
├── .env.example             # Example template env configuration
├── requirements.txt         # Dependent libraries
├── README.md                # System documentation
└── app.py                   # Entrypoint router script
```

---

## 🛠️ Installation & Setup

### Prerequisites

Ensure you have **Python 3.10+** installed on your system.

### 1. Clone or Extract the Project

Clone this repository or extract the project folder to your local machine.

### 2. Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

1. Copy `.env.example` to create a `.env` file:
   ```bash
   cp .env.example .env
   ```
2. Open the `.env` file and insert your OpenAI API Key:
   ```env
   OPENAI_API_KEY=your_actual_openai_key_here
   MODEL_NAME=gpt-4o-mini
   ```
   > 💡 **Note:** If no `OPENAI_API_KEY` is added or if the connection fails, the chatbot operates in **Local Advisor Mode** using intelligent predefined student rules, allowing you to fully test the interface.

---

## ⚡ How to Run

Launch the Streamlit server from the project directory:

```bash
streamlit run app.py
```

The application will open automatically in your browser at `http://localhost:8501`.

---

## 🔐 Security & Error Handling

* **Password Security**: Student passwords are salted and hashed using `bcrypt` prior to database writes. Plaintext passwords are never saved.
* **Input Checks**: Registration filters require valid email format matching (`@`), matching confirmation codes, and a minimum password length of 8 characters containing numbers and letters.
* **Data Integrity**: JSON files are checked on start. If corrupt or missing, they are automatically initialized to prevent application crashes.
* **Key Hiding**: API keys are loaded strictly from the environment using `python-dotenv`.

---

## 📈 Future Improvements

* Integrate relational database wrappers (PostgreSQL/MySQL) for larger student cohorts.
* Connect canvas LMS APIs to synchronize live assignment due dates.
* Incorporate OCR scanners for students to upload exam syllabi to the AI Assistant.

---

## 📄 License

This project is licensed under the MIT License.
