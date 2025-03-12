# app/main.py
from fastapi import FastAPI
from app.routes import use_cases, auth, users, institutions, ai_technology, use_case_ai_technology
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# Allow CORS for Vue.js frontend (adjust origins in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "https://uniai-frontend.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app/main.py
@app.get("/test")
def test_endpoint():
    return {"message": "API is working!"}


app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(users.router, prefix="/api", tags=["users"])
app.include_router(use_cases.router, prefix="/api", tags=["use_cases"])
app.include_router(institutions.router, prefix="/api", tags=["institutions"])
app.include_router(ai_technology.router, prefix="/api", tags=["ai-technologies"])
app.include_router(use_case_ai_technology.router, prefix="/api", tags=["use-case-ai-tech"])