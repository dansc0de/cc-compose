# syntax=docker/dockerfile:1

##########################
# Build Stage
##########################
FROM python:3.11-buster as builder

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --upgrade pip && pip install poetry

COPY pyproject.toml poetry.lock* ./

# configure and install poetry dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

# copy all the application code
COPY . .

##########################
# Final Stage
##########################
FROM python:3.11-buster as final

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# copy the installed dependencies from the builder stage, as well as the application code
COPY --from=builder /usr/local /usr/local
COPY --from=builder /app /app

EXPOSE 8000

# run our application
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["uvicorn", "cc_compose.server:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
