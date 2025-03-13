# app/main.py
from fastapi import FastAPI, Depends
from fastapi.openapi.utils import get_openapi
from app.routes import use_cases, auth, users, institutions, ai_technology, use_case_ai_technology
from fastapi.middleware.cors import CORSMiddleware
from app.routes.auth import oauth2_scheme

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="AI Use Case Tracker API",
        version="1.0.0",
        description="API documentation for managing AI use cases",
        routes=app.routes,
    )
    
    # Add security scheme
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    
    # Add security requirements to all protected paths
    protected_paths = ["/api/use-cases/", "/api/use-cases/{use_case_id}"]
    for path in openapi_schema["paths"]:
        if any(p in path for p in protected_paths):
            for method in openapi_schema["paths"][path]:
                if method in ["post", "put", "delete"]:
                    openapi_schema["paths"][path][method]["security"] = [{"BearerAuth": []}]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app = FastAPI()
app.openapi = custom_openapi 

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
app.include_router(use_cases.router, prefix="/api", tags=["use-cases"])
app.include_router(institutions.router, prefix="/api", tags=["institutions"])
app.include_router(ai_technology.router, prefix="/api", tags=["ai-technologies"])
app.include_router(use_case_ai_technology.router, prefix="/api", tags=["use-case-ai-tech"])