# app/main.py
from fastapi import FastAPI
from backend.app.routes.use_cases import router as use_cases_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# Allow CORS for Vue.js frontend (adjust origins in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://uniai-frontend.onrender.com"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# app/main.py
@app.get("/test")
def test_endpoint():
    return {"message": "API is working!"}


app.include_router(use_cases_router, prefix="/api")