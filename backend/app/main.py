from fastapi import FastAPI, Depends
from fastapi.openapi.utils import get_openapi
from app.routes import projects, auth, users, institutions, ai_technology, project_ai_technology, search
from fastapi.middleware.cors import CORSMiddleware
from app.routes.auth import oauth2_scheme
from services.elastic_search_service import initialize_index, check_index_status
from services.event_service import event_dispatcher
from services.elastic_sync_service import register_elasticsearch_listeners

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="AI Project Tracker API",
        version="1.0.0",
        description="API documentation for managing AI projects",
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
    
    # Add security requirements to the next paths
    protected_paths = ["/api/projects/", "/api/projects/{project_id}"]
    for path in openapi_schema["paths"]:
        if any(p in path for p in protected_paths):
            for method in openapi_schema["paths"][path]:
                # Only add security for methods that modify data, excluding get all, get by id and get by user id
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


# Initialize Elasticsearch index and event dispatcher
@app.on_event("startup")
async def startup_db_client():
    try:
        await initialize_index()
        # Check index status after initialization
        status = await check_index_status()
        print(f"Elasticsearch index status: {status['status']}")
        print(f"Document count: {status.get('document_count', 0)}")
        
        # Register Elasticsearch event listeners
        register_elasticsearch_listeners()
        # Start the event dispatcher
        event_dispatcher.start()
        print("Event dispatcher started")
    except Exception as e:
        print(f"Error initializing services: {e}")

# Shutdown event dispatcher
@app.on_event("shutdown")
async def shutdown_event():
    try:
        await event_dispatcher.stop()
        print("Event dispatcher stopped")
    except Exception as e:
        print(f"Error shutting down event dispatcher: {e}")

# app/main.py
@app.get("/test")
def test_endpoint():
    return {"message": "API is working!"}


app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(users.router, prefix="/api", tags=["users"])
app.include_router(projects.router, prefix="/api", tags=["projects"])
app.include_router(institutions.router, prefix="/api", tags=["institutions"])
app.include_router(ai_technology.router, prefix="/api", tags=["ai-technologies"])
app.include_router(project_ai_technology.router, prefix="/api", tags=["project-ai-tech"])
app.include_router(search.router, prefix="/api", tags=["search"])