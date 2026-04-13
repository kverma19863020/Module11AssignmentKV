# Module 11 Reflection

## Overview
This module focused on building a Calculation model using SQLAlchemy, validating
input with Pydantic schemas, implementing a Factory Pattern, and wiring everything
into a CI/CD pipeline with GitHub Actions and Docker Hub.

## Key Experiences

### Calculation Model
I chose to both store the result at insert time and expose a compute() method
for on-demand recalculation. Using SAEnum tied to a Python str enum kept
SQLAlchemy and Pydantic aligned without manual mapping.

### Pydantic Schemas
Using model_validator in Pydantic v2 was necessary to enforce the divide-by-zero
constraint across two fields at once, since field_validator only sees one field
at a time.

### Factory Pattern
The CalculationFactory uses a registry dictionary mapping OperationType to
Operation subclasses. Adding a new operation only requires one new class and
one dictionary entry without touching existing code.

## Challenges

- Shell commands accidentally got written into Python files causing NameError
  during test collection. Fixed by verifying each file with head -1 before committing.
- GitHub rejected password authentication for git push. Required a Personal
  Access Token with repo and workflow scopes.
- Docker login failed in CI until DOCKER_USERNAME and DOCKER_PASSWORD were
  added as GitHub repository secrets using a Docker Hub access token.
- psycopg2 import failed at module load time in CI until psycopg2-binary was
  added to requirements.txt and DATABASE_URL was set before pytest ran.

## What I Would Improve
Add Alembic migrations, a shared conftest.py for fixtures, and a
docker-compose.yml for easier local development.
