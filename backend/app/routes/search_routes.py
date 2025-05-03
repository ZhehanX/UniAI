from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from services.elastic_search_service import search_projects

router = APIRouter()

@router.get("/")
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