# 🛟 Social Assistance Finder API

The **Social Assistance Finder** is a backend application built using **FastAPI** and **PostgreSQL** that connects individuals in need with NGOs offering critical services such as shelter, food, mental health support, rehabilitation, and medical guidance.

This API facilitates a secure, scalable, and intelligent matching system with support for JWT-based authentication, role-based access, and AI-powered NGO recommendations.

---

## 🚀 Features

- 🔐 **JWT Authentication**
  - Signup, Login, Secure endpoints
- 🧑‍🤝‍🧑 **User Roles**
  - `needy_person` and `ngo`
- 🧠 **AI/GenAI-Based Matching**
  - Recommend NGOs based on user needs and location
- 📋 **Support Requests**
  - Users can create requests for food, shelter, mental health, etc.
- 📦 **NGO Service Management**
  - NGOs can register services they offer
- 🧪 **Test Coverage**
  - Pytest with CI/CD integration
- ☁️ **Deployment Ready**
  - Works on Render/Vercel with environment variables

---

## 🏗️ Tech Stack

- **Backend:** FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLModel (Pydantic + SQLAlchemy)
- **Auth:** OAuth2 with JWT Tokens
- **Testing:** Pytest
- **CI/CD:** GitHub Actions
- **Deployment:** Render / Vercel (API-only)

---

## 📁 Project Structure
app/
├── models/                # SQLModel classes
├── routers/               # API route files
├── services/              # Business logic & AI matching
├── auth/                  # JWT auth handling
├── database.py            # DB setup
├── main.py                # FastAPI app
tests/
├── test_user.py           # Unit tests
.env                       # Environment variables
requirements.txt
---

## ⚙️ Environment Variables

Use a `.env` file for secrets:
DATABASE_URL=postgresql://user:password@localhost:5432/social_assistance_db
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

---

## 🧪 Run Locally

1. Clone the repo:
```bash
git clone https://github.com/neha singhal/social-assistance-finder.git
cd social-assistance-finder

2.	Install dependencies:
pip install -r requirements.txt

3.	Set up .env file with your DB and JWT credentials.
	
4.	Run the app
uvicorn app.main:app --reload:

5.	Access docs:
http://127.0.0.1:8000/docs

🧪 Run Tests
pytest
✅ CI/CD with GitHub Actions automatically runs tests on each push to main.
🔐 API Authentication (JWT)
	•	POST /users → Register user
	•	POST /users/token → Login & get JWT
	•	GET /users/me → Current user info

Use the JWT as a Bearer token in headers:

🛠️ Deployment

You can deploy to:
	•	Render
	•	Vercel (with serverless FastAPI)
	•	Docker-compatible VPS

Sample command for Render:
# render.yaml
services:
  - type: web
    name: social-assistance-finder
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port 10000

👥 Contributors
	•	Neha Singhal

📄 License

MIT License. Feel free to use, modify, and distribute.


