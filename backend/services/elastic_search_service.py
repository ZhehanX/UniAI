import os
from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk
import ssl
import certifi

# Create Elasticsearch client with Elastic Cloud configuration
cloud_id = os.environ.get("ELASTIC_CLOUD_ID")
cloud_username = os.environ.get("ELASTIC_CLOUD_USERNAME", "elastic")
cloud_password = os.environ.get("ELASTIC_CLOUD_PASSWORD")

# Use Elastic Cloud if credentials are provided, otherwise fallback to local
if cloud_id and cloud_password:
    client = AsyncElasticsearch(
        cloud_id=cloud_id,
        basic_auth=(cloud_username, cloud_password),
        ssl_context=ssl.create_default_context(cafile=certifi.where())
    )
    print("Connected to Elastic Cloud")
else:
    # Fallback to local for development
    client = AsyncElasticsearch([os.environ.get("ELASTICSEARCH_URL", "http://localhost:9200")])
    print("Connected to local Elasticsearch")

# Initialize Elasticsearch index for projects
async def initialize_index():
    index_exists = await client.indices.exists(index="projects")
    
    if not index_exists:
        await client.indices.create(
            index="projects",
            body={
                "mappings": {
                    "properties": {
                        "title": {"type": "text"},
                        "short_description": {"type": "text"},
                        "full_description": {"type": "text"},
                        "institution": {
                            "properties": {
                                "name": {"type": "text"},
                                "city": {"type": "text"},
                                "state": {"type": "text"},
                                "country": {"type": "text"}
                            }
                        },
                        "ai_technologies_names": {"type": "text"},
                        "contact": {"type": "text"},
                        "url": {"type": "text"},
                        "status": {"type": "keyword"},
                        "created_at": {"type": "date"}
                    }
                }
            }
        )
        print("Projects index created")

# Index a project document
async def index_project(project):
    await client.index(
        index="projects",
        id=project["id"],
        body=project
    )
    
    # Refresh the index to make the document available for search
    await client.indices.refresh(index="projects")

# Update a project document
async def update_project(project_id, project_data):
    await client.update(
        index="projects",
        id=project_id,
        body={"doc": project_data},
        refresh=True
    )
    return {"status": "updated", "id": project_id}

# Delete a project document
async def delete_project(project_id):
    await client.delete(
        index="projects",
        id=project_id,
        refresh=True
    )
    return {"status": "deleted", "id": project_id}

# Search projects
async def search_projects(query):
    response = await client.search(
        index="projects",
        body={
            "query": {
                "bool": {
                    "should": [
                        {"match": {"title": {"query": query, "boost": 3}}},
                        {"match": {"short_description": {"query": query, "boost": 2}}},
                        {"match": {"full_description": query}},
                        {"match": {"institution.name": {"query": query, "boost": 2}}},
                        {"match": {"institution.city": query}},
                        {"match": {"institution.state": query}},
                        {"match": {"institution.country": query}},
                        {"match": {"ai_technologies_names": {"query": query, "boost": 3}}}
                    ],
                    "minimum_should_match": 1, # at least one match else it will return all projects
                    "filter": [
                        {"term": {"status": "approved"}}
                    ]
                }
            },
            "highlight": {
                "fields": {
                    "title": {},
                    "short_description": {},
                    "institution.name": {},
                    "ai_technologies_names": {},
                }
            }
        }
    )

    return [
        {
            **hit["_source"],
            "score": hit["_score"],
            "highlights": hit.get("highlight", {})
        }
        for hit in response["hits"]["hits"]
    ]

# Bulk index projects
async def bulk_index_projects(projects):
    operations = []
    for project in projects:
        operations.append({"index": {"_index": "projects", "_id": project["id"]}})
        operations.append(project)
    
    response = await client.bulk(body=operations, refresh=True)
    
    if response.get("errors"):
        errored_documents = []
        for i, item in enumerate(response["items"]):
            operation = list(item.keys())[0]
            if item[operation].get("error"):
                errored_documents.append({
                    "status": item[operation]["status"],
                    "error": item[operation]["error"],
                    "document": operations[i * 2 + 1]
                })
        print("Failed to index some documents", errored_documents)
    
    return response

# Add this function to check index status
async def check_index_status():
    exists = await client.indices.exists(index="projects")
    if not exists:
        return {"status": "index_not_found", "message": "Projects index does not exist"}
    
    # Get document count
    count = await client.count(index="projects")
    
    # Get index settings and mappings
    settings = await client.indices.get_settings(index="projects")
    mappings = await client.indices.get_mapping(index="projects")
    
    return {
        "status": "ok",
        "exists": exists,
        "document_count": count["count"],
        "settings": settings,
        "mappings": mappings
    }

# Add a simple search function for testing
async def simple_search():
    try:
        response = await client.search(
            index="projects",
            body={
                "query": {
                    "match_all": {}
                },
                "size": 10
            }
        )
        
        return [
            {
                **hit["_source"],
                "score": hit["_score"]
            }
            for hit in response["hits"]["hits"]
        ]
    except Exception as e:
        print(f"Search error: {str(e)}")
        return {"error": str(e)}

# Advanced search projects with specific field filters
async def advanced_search_projects(filters):
    """
    Perform advanced search with specific field filters
    
    Args:
        filters (dict): Dictionary containing field-specific search terms
            Possible keys: title, institution, technology, location, etc.
    
    Returns:
        list: List of matching projects with highlights
    """
    # Build the query based on provided filters
    should_clauses = []
    must_clauses = []
    
    # Process title filter
    if "title" in filters and filters["title"]:
        must_clauses.append({
            "match": {
                "title": {
                    "query": filters["title"],
                    "boost": 3
                }
            }
        })
    
    # Process institution filter
    if "institution" in filters and filters["institution"]:
        institution_query = filters["institution"]
        should_clauses.extend([
            {"match": {"institution.name": {"query": institution_query, "boost": 3}}}
        ])
        # If we have institution filters, at least one should match
        must_clauses.append({
            "bool": {
                "should": should_clauses,
                "minimum_should_match": 1
            }
        })
        # Reset should_clauses after adding to must
        should_clauses = []
    
    # Process AI technology filter
    if "technology" in filters and filters["technology"]:
        tech_query = filters["technology"]
        must_clauses.append({
            "bool": {
                "should": [
                    {"match": {"ai_technologies_names": {"query": tech_query, "boost": 2}}}
                ],
                "minimum_should_match": 1
            }
        })
    
    # Process location filter
    if "location" in filters and filters["location"]:
        location_query = filters["location"]
        location_should = [
            {"match": {"institution.city": {"query": location_query, "boost": 2}}},
            {"match": {"institution.state": {"query": location_query, "boost": 1.5}}},
            {"match": {"institution.country": {"query": location_query, "boost": 1}}}
        ]
        must_clauses.append({
            "bool": {
                "should": location_should,
                "minimum_should_match": 1
            }
        })
    
    # Build the final query
    query = {
        "bool": {
            "filter": [
                {"term": {"status": "approved"}}
            ]
        }
    }
    
    # Add must clauses if we have any
    if must_clauses:
        query["bool"]["must"] = must_clauses
    
    # If no specific filters were provided, return an empty result
    if not must_clauses:
        return []
    
    # Execute the search
    response = await client.search(
        index="projects",
        body={
            "query": query,
            "highlight": {
                "fields": {
                    "title": {},
                    "short_description": {},
                    "institution.name": {},
                    "institution.city": {},
                    "institution.country": {}
                }
            }
        }
    )
    
    # Process and return results
    return [
        {
            **hit["_source"],
            "score": hit["_score"],
            "highlights": hit.get("highlight", {})
        }
        for hit in response["hits"]["hits"]
    ]