from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
import uuid
from workers.processor import task_processor
from services.database import get_task_result, save_task_result

router = APIRouter(prefix="/api", tags=["tasks"])

class TaskRequest(BaseModel):
    data_source: Optional[str] = "dummy"
    params: Optional[Dict[str, Any]] = {}

class TaskResponse(BaseModel):
    task_id: str
    status: str
    message: str

@router.post("/run-task", response_model=TaskResponse)
async def run_task(request: TaskRequest):
    """
    Main endpoint: POST /run-task
    Creates a new task and queues it for processing
    """
    # Generate unique task ID
    task_id = f"task_{uuid.uuid4().hex[:8]}"
    
    # Create initial task record
    save_task_result(task_id, "queued")
    
    # Add to processing queue
    task_params = {
        "data_source": request.data_source,
        **request.params
    }
    await task_processor.add_task(task_id, task_params)
    
    return TaskResponse(
        task_id=task_id,
        status="queued",
        message=f"Task {task_id} queued for processing"
    )

@router.get("/task/{task_id}")
async def get_task_status(task_id: str):
    """
    Get task status and results
    """
    result = get_task_result(task_id)
    
    if not result:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return result

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "automation-agent"}