# Backend with AIOHTTP

This is a simple Trello-like task management backend built using **AIOHTTP**, **SQLite**, and **AIOSQLITE**.

---

## 🚀 Features

- Board and Task CRUD operations
- SQLite lightweight database
- SPA-friendly (serves index.html on unknown routes)
- CORS enabled for frontend development
- Environment variable for frontend path

---

## 📦 Requirements

- Python 3.8+
- pip

---

## 🔧 Setup

1. **Clone the repository**:

   ```bash
   git clone https://github.com/HarshithPrathi30/TaskManagement_BackEnd.git
   cd backend_Directory_Name
   ```

2. **Create a virtual environment(recommended)**:

   ```python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:

   `pip install -r requirements.txt`

4. **Set the frontend path**:

   ```Edit or create a .env file:  (Currently not mandatory, but required when both frontend and backend runs on same port.)
   FRONTEND_PATH=Frontend/frontend/public/index.html
   ```

5. **Ensure your SQLite schema file exists**:

   ```Create schema.sql with the required tables as in schema.sql

   ```

6. **Run the app**:
   `python app.py`
