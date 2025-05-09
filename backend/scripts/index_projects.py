import asyncio
import sys
import os

# Add the parent directory to sys.path to allow relative imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.elastic_search_service import bulk_index_projects, initialize_index
from app.crud.project_crud import get_projects
from app.database import SessionLocal

async def index_all_projects():
    try:
        # Initialize the index
        await initialize_index()
        
        # Create a database session
        db = SessionLocal()
        
        # Get all projects from your database
        projects = get_projects(db)
        
        # Convert SQLAlchemy objects to dictionaries
        project_dicts = []
        for project in projects:
            # Handle full_description
            full_description_text = ""
            if project.full_description and isinstance(project.full_description, dict) and 'value' in project.full_description:
                full_description_text = project.full_description['value']
            elif isinstance(project.full_description, str):
                full_description_text = project.full_description
            
            project_dict = {
                "id": project.id,
                "title": project.title,
                "short_description": project.short_description,
                "full_description": full_description_text,  # Use the extracted text value
                "institution_id": project.institution_id,
                "contact": project.contact,
                "url": project.url,
                "status": project.status,
                "created_at": project.date_created.isoformat() if project.date_created else None
            }
            
            # Add AI technologies if they exist
            if project.ai_technologies:
                project_dict["ai_technologies"] = [tech.ai_technology_id for tech in project.ai_technologies]
            
            project_dicts.append(project_dict)
        
        print(f"Indexing {len(project_dicts)} projects...")
        
        # Bulk index the projects
        result = await bulk_index_projects(project_dicts)
        
        print("Indexing complete!")
        print(result)
    except Exception as error:
        print(f"Error indexing projects: {error}")
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(index_all_projects())