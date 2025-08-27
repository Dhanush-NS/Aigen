Backend → FastAPI + PostgreSQL + JWT auth + MCP integration (DuckDuckGo + Flux ImageGen, with fallbacks)

Frontend → React + Tailwind CSS

Database → PostgreSQL (users + history)

Here’s a polished README.md you can use directly on GitHub 👇

🚀 AI-Powered Content & Image Explorer

An AI-powered full-stack application where users can:

🔍 Perform web searches (via MCP DuckDuckGo server with fallback to DuckDuckGo API)

🖼️ Generate AI images from text (via MCP Flux server with fallback to Pollinations)

📜 Manage their search & image history in a personalized dashboard

🔐 Register/Login securely with JWT authentication

💻 Enjoy a clean React + Tailwind CSS frontend

🌟 Features

User Authentication: Register/Login with JWT-secured routes

Search: Ask any query, results from DuckDuckGo MCP (or fallback API)

Image Generation: Generate AI images from prompts with Flux MCP (or fallback Pollinations API)

Dashboard: View, filter, and delete your saved searches & generated images

Database Persistence: PostgreSQL stores users, history, and metadata

Responsive UI: React + Tailwind for a clean, mobile-friendly experience

🏗️ Tech Stack

Frontend: React, Tailwind CSS

Backend: FastAPI (Python)

Database: PostgreSQL (SQLAlchemy ORM)

Authentication: JWT (OAuth2 Password Flow)

MCP Servers:

🔍 DuckDuckGo MCP

🖼️ Flux ImageGen MCP

Fallback APIs: DuckDuckGo API & Pollinations

⚙️ Installation
1. Clone the Repository
git clone https://github.com/<your-username>/ai-content-explorer.git
cd ai-content-explorer

2. Backend Setup (FastAPI)
cd backend
python -m venv .venv
source .venv/bin/activate    # (Windows: .venv\Scripts\activate)

pip install -r requirements.txt


Set up PostgreSQL and update backend/database.py with your DB URL:

SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://<user>:<password>@localhost:5432/aigen"


Run the backend:

uvicorn backend.main:app --reload


FastAPI will be live at 👉 http://127.0.0.1:8000

Swagger Docs 👉 http://127.0.0.1:8000/docs

3. Frontend Setup (React + Tailwind)
cd frontend
npm install
npm run dev


Frontend will be live at 👉 http://localhost:5173

🔑 Authentication

Register: POST /auth/register

Login: POST /auth/login → returns JWT token

Use token as:

Authorization: Bearer <your_token>

📸 Screenshots (Optional)

Login Page

Dashboard (Search & Images)

Image Generation Example
