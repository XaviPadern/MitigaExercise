from . import models, schemas, database

from sqlalchemy.orm import Session
from fastapi import HTTPException
from contextlib import contextmanager


@contextmanager
def get_session():
    db = next(database.get_db())
    try:
        yield db
    finally:
        db.close()


def get_task(task_id: int):
    with get_session() as db:
        return get_task_private(task_id, db)


def get_tasks(skip: int = 0, limit: int = 10):
    with get_session() as db:
        return db.query(models.Task).offset(skip).limit(limit).all()


def create_task(task: schemas.TaskCreate):

    with get_session() as db:

        # Title length validation
        if len(task.title) < 5 or len(task.title) > 50:
            raise HTTPException(
                status_code=400, detail="Title length must be between 5 and 50 characters")

        # Description length validation
        if len(task.description) < 10:
            raise HTTPException(
                status_code=400, detail="Description length must be at least 10 characters")

        db_task = models.Task(
            title=task.title, description=task.description, completed=task.completed)
        
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task


def update_task(task: schemas.TaskCreate, task_id: int):

    with get_session() as db:

        db_task = get_task_private(task_id, db)

        db_task.title = task.title
        # missing field here! (description)
        db_task.description = task.description        
        db_task.completed = task.completed
        
        db.commit()
        db.refresh(db_task)

        return db_task
    

def delete_task(task_id: int):

    with get_session() as db:

        db_task = get_task_private(task_id, db)
        db.delete(db_task)
        db.commit()

        return db_task
    

def get_task_private(task_id: int, db: Session):
        
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()

    if db_task is None:
        raise HTTPException(status_code=400, detail="Task not found")
    
    return db_task