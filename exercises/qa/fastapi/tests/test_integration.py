from sqlalchemy import create_engine, MetaData, Table

from exercises.qa.fastapi.app import schemas

def reset_table():
    # Create an engine
    engine = create_engine("postgresql://admin:1234@localhost/testdb")

    # Reflect the current database schema
    metadata = MetaData()
    metadata.reflect(bind=engine)

    # Access the "tasks" table
    tasks_table = Table('tasks', metadata, autoload_with=engine)

    # Delete all records from the "tasks" table
    with engine.connect() as connection:
        delete_statement = tasks_table.delete()
        connection.execute(delete_statement)
        connection.commit()  # Explicitly commit the transaction
        print("Table reset.")
    

def test_given_empty_database_when_task_is_created_then_it_is_added_to_the_database(client):
    """Test the read operation on the main endpoint."""

    reset_table()

    title = "New Task"
    description = "This is a new task."
    completed = True

    data = {
        "title": title,
        "description": description,
        "completed": f"{completed}"
    }

    response = client.post("/tasks", json=data)

    assert response.status_code == 200
    task = schemas.Task.model_validate(response.json())
    
    # Example assertion (adjust according to your schemas.Task model fields)
    assert task.title == title
    assert task.description == description
    assert task.completed == completed

    response = client.get("/tasks")

    assert response.status_code == 200
    
    tasks = [schemas.Task(**item) for item in response.json()]

    assert len(tasks) == 1, "The list should contain exactly one task."

    task = tasks[0]

    # id cannot be asserted because it is dynamically generated

    assert task.title == title
    assert task.description == description
    assert task.completed == completed


