################################################
# This is the webserver. Do not alter this file.
################################################
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from cc_compose.models import TaskCreate, TaskRead
from cc_compose.database import init_db, get_db_connection

# init
init_db()

app = FastAPI()

# mount UI static files
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=FileResponse)
async def serve_ui():
    """
    Serve the main UI page.
    """
    return FileResponse("static/index.html")


@app.get("/healthz", response_class=JSONResponse)
async def serve_ui():
    """
    Serve the main UI page.
    """
    return JSONResponse(content={"status": "ok"})


# POST
@app.post("/tasks", response_model=TaskRead)
async def create_task(task_data: TaskCreate):
    """
    Create a new task.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tasks (title, description, completed) VALUES (%s, %s, %s) RETURNING id",
        (task_data.title, task_data.description, task_data.completed),
    )
    task_id = cursor.fetchone()['id']
    conn.commit()
    conn.close()

    return TaskRead(id=task_id, **task_data.dict())


# GET
@app.get("/tasks", response_model=list[TaskRead])
async def get_tasks():
    """
    Retrieve all tasks.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()
    conn.close()

    return [
        TaskRead(
            id=row["id"],
            title=row["title"],
            description=row["description"],
            completed=bool(row["completed"]),
        )
        for row in rows
    ]


# UPDATE
@app.put("/tasks/{task_id}", response_model=TaskRead)
async def update_task(task_id: int, task_data: TaskCreate):
    """
    Update a task by its ID.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
    existing_task = cursor.fetchone()

    if not existing_task:
        conn.close()
        raise HTTPException(status_code=404, detail="Task not found")

    cursor.execute(
        "UPDATE tasks SET title = %s, description = %s, completed = %s WHERE id = %s",
        (task_data.title, task_data.description, task_data.completed, task_id),
    )
    conn.commit()
    conn.close()

    return TaskRead(id=task_id, **task_data.dict())


# DELETE
@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    """
    Delete a task by its ID.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
    existing_task = cursor.fetchone()

    if not existing_task:
        conn.close()
        raise HTTPException(status_code=404, detail="Task not found")

    cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    conn.commit()
    conn.close()

    return {"message": f"Task {task_id} deleted successfully"}
