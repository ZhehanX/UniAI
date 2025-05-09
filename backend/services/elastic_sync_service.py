from services.event_service import event_dispatcher, PROJECT_CREATED, PROJECT_UPDATED, PROJECT_DELETED
from services.elastic_search_service import index_project, update_project, delete_project

async def format_project_for_elasticsearch(project):
    """Format a project object for Elasticsearch indexing"""
    # Extract full description text
    full_description_text = ""
    if project.full_description and isinstance(project.full_description, dict) and 'value' in project.full_description:
        full_description_text = project.full_description['value']
    elif isinstance(project.full_description, str):
        full_description_text = project.full_description
    
    # Create the project dictionary
    project_dict = {
        "id": project.id,
        "title": project.title,
        "short_description": project.short_description,
        "full_description": full_description_text,
        "institution_id": project.institution_id,
        "contact": project.contact,
        "url": project.url,
        "status": project.status,
        "created_at": project.date_created.isoformat() if project.date_created else None
    }
    # Add institution details if exist
    if project.institution:
        project_dict["institution"] = {
            "name": project.institution.name,
            "city": project.institution.city,
            "state": project.institution.state,
            "country": project.institution.country
        } 

    # Add AI technologies if exist
    if project.ai_technologies:
        project_dict["ai_technologies_names"] = [tech.ai_technology.name for tech in project.ai_technologies]

    return project_dict

async def handle_project_created(project):
    """Handle project created event"""
    project_dict = await format_project_for_elasticsearch(project)
    await index_project(project_dict)
    print(f"Indexed project {project.id} in Elasticsearch")

async def handle_project_updated(project):
    """Handle project updated event"""
    project_dict = await format_project_for_elasticsearch(project)
    await update_project(project.id, project_dict)
    print(f"Updated project {project.id} in Elasticsearch")

async def handle_project_deleted(project_id):
    """Handle project deleted event"""
    await delete_project(project_id)
    print(f"Deleted project {project_id} from Elasticsearch")

def register_elasticsearch_listeners():
    """Register all Elasticsearch event listeners"""
    event_dispatcher.register(PROJECT_CREATED, handle_project_created)
    event_dispatcher.register(PROJECT_UPDATED, handle_project_updated)
    event_dispatcher.register(PROJECT_DELETED, handle_project_deleted)