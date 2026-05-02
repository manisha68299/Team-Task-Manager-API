from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, List

import models
import schemas
import auth
from database import get_db
from models import TaskStatus

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model=schemas.TaskResponse, status_code=201)
def create_task(
    task_data:    schemas.TaskCreate,
    db:           Session      = Depends(get_db),
    current_user: models.User  = Depends(auth.get_current_active_user)
):
    new_task = models.Task(
        title=task_data.title,
        description=task_data.description,
        is_priority=task_data.is_priority,
        owner_id=current_user.id,
        status=TaskStatus.TODO
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


@router.get("/", response_model=List[schemas.TaskResponse])
def list_my_tasks(
    status:      Optional[TaskStatus] = Query(default=None, description="Filter by status"),
    is_priority: Optional[bool]       = Query(default=None, description="Filter by priority"),
    search:      Optional[str]        = Query(default=None, max_length=100, description="Search in title"),
    skip:        int                  = Query(default=0, ge=0, description="Items to skip"),
    limit:       int                  = Query(default=10, ge=1, le=100, description="Max items to return"),
    db:          Session              = Depends(get_db),
    current_user: models.User         = Depends(auth.get_current_active_user)
):
    query = db.query(models.Task).filter(models.Task.owner_id == current_user.id)

    if status is not None:
        query = query.filter(models.Task.status == status)
    if is_priority is not None:
        query = query.filter(models.Task.is_priority == is_priority)
    if search is not None:
        query = query.filter(models.Task.title.ilike(f"%{search}%"))

    return query.order_by(models.Task.created_at.desc()).offset(skip).limit(limit).all()


@router.get("/stats")
def get_my_task_stats(
    db:           Session     = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    results = db.query(
        models.Task.status,
        func.count(models.Task.id).label("count")
    ).filter(
        models.Task.owner_id == current_user.id
    ).group_by(models.Task.status).all()

    stats = {row.status.value: row.count for row in results}
    total = db.query(func.count(models.Task.id)).filter(
        models.Task.owner_id == current_user.id
    ).scalar()

    return {"total": total, "by_status": stats, "user": current_user.username}


@router.get("/{task_id}", response_model=schemas.TaskResponse)
def get_task(
    task_id:      int,
    db:           Session     = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.owner_id == current_user.id
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return task


@router.patch("/{task_id}", response_model=schemas.TaskResponse)
def update_task(
    task_id:     int,
    task_update: schemas.TaskUpdate,
    db:           Session     = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.owner_id == current_user.id
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

    for field, value in task_update.model_dump(exclude_unset=True).items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id:      int,
    db:           Session     = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.owner_id == current_user.id
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

    db.delete(task)
    db.commit()
    return None
