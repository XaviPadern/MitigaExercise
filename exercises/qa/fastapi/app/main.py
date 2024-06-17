from . import models, schemas, crud, database

from fastapi import FastAPI


app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)


# error found here with a final slash (/)
#@app.post("/tasks/", response_model=schemas.Task
@app.post("/tasks", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate):
    return crud.create_task(task=task)

@app.get("/tasks/{task_id}", response_model=schemas.Task)
def read_task(task_id: int):
    return crud.get_task(task_id=task_id)

# error found here with a final slash (/)
#@app.get("/tasks/", response_model=list[schemas.Task])
@app.get("/tasks", response_model=list[schemas.Task])
def read_tasks(skip: int = 0, limit: int = 10):
    return crud.get_tasks(skip=skip, limit=limit)

@app.put("/tasks/{task_id}", response_model=schemas.Task)
def update_task(task_id: int, task: schemas.TaskCreate):    
    return crud.update_task(task=task, task_id=task_id)

@app.delete("/tasks/{task_id}", response_model=schemas.Task)
def delete_task(task_id: int):
    return crud.delete_task(task_id=task_id)
