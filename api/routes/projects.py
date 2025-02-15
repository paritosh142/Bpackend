from fastapi import APIRouter, HTTPException, Query
from api.database import db
from api.models import ProjectBase as Project
from datetime import datetime
from bson import ObjectId
from typing import List
import random

router = APIRouter(prefix="/projects", tags=["projects"])

@router.get("/", response_model=List[dict])
async def get_projects():
    projects = []
    async for project in db.projects.find():
        project['_id'] = str(project['_id'])
        projects.append(project)
    return projects

@router.post("/", response_model=Project)
async def add_project(project: Project):
    project_data = project.dict()
    project_data['created_at'] = datetime.utcnow()
    await db.projects.insert_one(project_data)
    return {**project_data, "_id": str(project_data['_id'])}

@router.get("/random", response_model=List[dict])
async def get_random_projects(limit: int = Query(1, ge=1)):
    projects = []
    async for project in db.projects.find():
        project['_id'] = str(project['_id'])
        projects.append(project)
    
    if len(projects) < limit:
        raise HTTPException(status_code=400, detail="Not enough projects available")
    
    random_projects = random.sample(projects, limit)
    return random_projects

@router.get("/{project_id}", response_model=dict)
async def get_project(project_id: str):
    project = await db.projects.find_one({"_id": ObjectId(project_id)})
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    project['_id'] = str(project['_id'])
    return project

@router.put("/{project_id}", response_model=Project)
async def update_project(project_id: str, project: Project):
    update_data = project.dict()
    update_data['updated_at'] = datetime.utcnow()
    
    result = await db.projects.find_one_and_update(
        {"_id": ObjectId(project_id)},
        {"$set": update_data},
        return_document=True
    )
    
    if not result:
        raise HTTPException(status_code=404, detail="Project not found")
    result['_id'] = str(result['_id'])
    return result

@router.delete("/{project_id}")
async def delete_project(project_id: str):
    result = await db.projects.delete_one({"_id": ObjectId(project_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"message": "Project deleted successfully"}
