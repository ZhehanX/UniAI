import os
from elasticsearch import AsyncElasticsearch

# Create Elasticsearch client
client = AsyncElasticsearch([os.environ.get("ELASTICSEARCH_URL", "http://localhost:9200")])

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
                        "ai_technologies": {"type": "keyword"},
                        "contact": {"type": "text"},
                        "url": {"type": "text"},
                        "status": {"type": "keyword"},
                        "created_at": {"type": "date"},
                        "updated_at": {"type": "date"}
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
                        {"term": {"ai_technologies": {"value": query, "boost": 3}}}
                    ],
                    "minimum_should_match": 1, # this line require to have at least one match else it will return all projects
                    "filter": [
                        {"term": {"status": "pending"}}
                    ]
                }
            },
            "highlight": {
                "fields": {
                    "title": {},
                    "short_description": {},
                    "institution.name": {}
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