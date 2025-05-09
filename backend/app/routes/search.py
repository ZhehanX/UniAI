from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from services.elastic_search_service import search_projects, advanced_search_projects

router = APIRouter()

@router.get("/search")
async def search(q: Optional[str] = Query(None)):
    """Search endpoint for projects"""
    try:
        if not q:
            raise HTTPException(status_code=400, detail="Search query is required")
        
        results = await search_projects(q)
        return results
    except Exception as error:
        print(f"Search error: {error}")
        raise HTTPException(status_code=500, detail="An error occurred during search")

@router.get("/advanced-search")
async def advanced_search(
    title: Optional[str] = Query(None, description="Search by title"),
    institution: Optional[str] = Query(None, description="Search by institution"),
    technology: Optional[str] = Query(None, description="Search by AI technology"),
    location: Optional[str] = Query(None, description="Search by location")
):
    """
    Advanced search with specific field filters
    """
    # Build filters dictionary from non-empty parameters
    filters = {}
    if title:
        filters["title"] = title
    if institution:
        filters["institution"] = institution
    if technology:
        filters["technology"] = technology
    if location:
        filters["location"] = location
    
    # If no filters provided, return empty results
    if not filters:
        return []
    
    results = await advanced_search_projects(filters)
    return results