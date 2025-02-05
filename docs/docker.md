# **Docker & Docker Compose Assignment: FastAPI and PostgreSQL**

## **Overview**

In this assignment, you will create a **Dockerfile** and complete a **Docker Compose** file to set up a FastAPI application with a PostgreSQL database. You will learn how to:

- Write a **multi-stage Dockerfile** for FastAPI.
- Use **Docker Compose** to define and orchestrate services.
- Add **service dependencies**, environment variables, and exposed ports.
- Start, stop, and inspect your containerized application.

You will be working with:

- `Dockerfile` (which you will create from scratch)
- `docker-compose.yml` (which you will complete by filling in the missing sections)

---

## **Documentation**
- [docker compose](https://docs.docker.com/compose/)
- [dockerfile](https://docs.docker.com/reference/dockerfile/)

---

## **1. Writing the Dockerfile**

Your first task is to create a **multi-stage Dockerfile** to build and run a FastAPI application. Implement the following:

### **🔹 Criteria to Complete the Dockerfile**

1. **Create a multi-stage Dockerfile** with two stages: `builder` and `app`.
    - **Use `python:3.11-buster` as the base image** in both the builder staging and the final app stage.
2. **Set** `WORKDIR` to **`/app`** in both stages.
3. **Install Poetry and upgrade pip** this needs to be done in the builder stage:
    - ```dockerfile
      pip install --upgrade pip && pip install poetry
      ```
4. **Build the application in a `builder` stage using Poetry**:
   - you need to copy the `pyproject.toml` and `poetry.lock` files to the builder stage before building.
   - ```dockerfile
      RUN poetry config virtualenvs.create false \
       && poetry install --no-root --no-interaction --no-ansi
     ```
5. Copy the code from the **/app** directory in builder stage to the **/app** stage:
    - Hint: Use the `COPY` command with a `--from=builder` to reference the builder stage context.
6. **Expose port 8000** for FastAPI to be accessible.
7. Set the **entrypoint.sh** as the **entrypoint** for the container:
8. Set the CMD parameter to run the FastAPI application:
    - uvicorn cc_compose.server:app --reload --host 0.0.0.0 --port 8000

---

## **2. Completing docker-compose.yml**

The provided `docker-compose.yml` file is missing key instructions. Complete it by filling in the missing sections.

### **🔹 FastAPI Service**

Modify the `fastapi` service in `docker-compose.yml` by adding:

- **`build.context: .`** to specify the directory of the Dockerfile.
- **Environment variables** to connect to the PostgreSQL database.
- **`depends_on: postgres`** to ensure the database is ready before FastAPI starts.
- **Exposed ports (********`8000:8000`********)** to make the FastAPI application accessible.

---

## **3. Running the Docker Compose Stack**

### **🔹 Start the Compose Stack**

```sh
 docker compose up --build
```

- This will **build the FastAPI image** and start all services.

### **🔹 Stop the Stack Without Removing Containers**

```sh
 docker compose stop
```

### **🔹 Shut Down the Stack and Remove Containers**

```sh
 docker compose down
```

- This will remove the containers but keep **volumes intact**.

### **🔹 Check Configuration Before Running**

```sh
 docker compose config
```

- Validates your `docker-compose.yml` file.

### **🔹 View Running Containers**

```sh
 docker ps
```

### **🔹 View Service Logs**

```sh
 docker compose logs -f
```

---

## **4. Verifying the Setup**

### **🔹 Check the FastAPI Healthcheck**

After starting the stack, confirm FastAPI is running:

```sh
 curl -f http://127.0.0.1:8000/healthz
```

### **🔹 Check PostgreSQL Status**

Run this inside the `postgres` container:

```sh
 docker exec -it <postgres_container_id> psql -U postgres -d tasksdb
```
