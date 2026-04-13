# Module11AssignmentKV

A FastAPI + SQLAlchemy + PostgreSQL service implementing a Calculation model
with Pydantic validation and a Factory Pattern for Add, Sub, Multiply, Divide.

## Docker Hub

https://hub.docker.com/r/kverma19863020/module11assignmentkv

## How to Run Tests Locally

### Step 1 - Clone the repo

    git clone https://github.com/kverma19863020/Module11AssignmentKV.git
    cd Module11AssignmentKV

### Step 2 - Create virtual environment and install dependencies

    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

### Step 3 - Start PostgreSQL using Docker

    docker run -d \
      --name postgres \
      -e POSTGRES_USER=user \
      -e POSTGRES_PASSWORD=password \
      -e POSTGRES_DB=calcdb \
      -p 5432:5432 \
      postgres:15

### Step 4 - Set the database URL

    export DATABASE_URL=postgresql://user:password@localhost:5432/calcdb

### Step 5 - Run unit tests

    pytest tests/test_unit_calculations.py -v

### Step 6 - Run integration tests

    pytest tests/test_integration_calculations.py -v

### Step 7 - Run all tests with coverage

    pytest --cov=app --cov-report=term-missing -v
