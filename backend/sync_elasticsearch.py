import asyncio
import sys
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud import project_crud
from services.event_service import event_dispatcher, PROJECT_CREATED
from services.elastic_sync_service import register_elasticsearch_listeners, format_project_for_elasticsearch
from services.elastic_search_service import initialize_index, bulk_index_projects, client, simple_search
from elasticsearch import AsyncElasticsearch

async def sync_projects():
    # Register Elasticsearch event listeners
    register_elasticsearch_listeners()
    
    # Initialize Elasticsearch index
    try:
        await initialize_index()
        print("Elasticsearch index initialized")
    except Exception as e:
        print(f"Error initializing Elasticsearch index: {e}")
        return
    
    # Get database session
    db = next(get_db())
    
    try:
        # Get all projects
        projects = project_crud.get_projects(db=db)
        print(f"Found {len(projects)} projects to synchronize")
        
        # Prepare project data for bulk indexing
        print("Preparing projects for bulk indexing...")
        project_dicts = []
        for i, project in enumerate(projects):
            try:
                print(f"Processing project {i+1}/{len(projects)}: {project.title}")
                project_dict = await format_project_for_elasticsearch(project)
                project_dicts.append(project_dict)
            except Exception as e:
                print(f"Error processing project {project.id} - {project.title}: {e}")
        
        # Bulk index all projects
        print(f"Bulk indexing {len(project_dicts)} projects...")
        result = await bulk_index_projects(project_dicts)
        print(f"Bulk indexing result: {result}")
        
        # Refresh the index - use the existing client instead of creating a new one
        await client.indices.refresh(index="projects")
        count_response = await client.count(index="projects")
        print(f"Elasticsearch document count: {count_response['count']}")
        
        # Test search to verify indexed data
        print("Testing search functionality...")
        search_results = await simple_search()
        print(f"Found {len(search_results)} documents in test search")
        
        print("Index refreshed")
        print("Synchronization complete!")
        
    except Exception as e:
        print(f"Error during synchronization: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(sync_projects())
