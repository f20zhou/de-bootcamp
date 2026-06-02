# DE Bootcamp -  data engineering portfolio

## Pipeline Architecture
Public API → Python ingestion → Postgres → dbt → Airflow

## Stack
- Python 3.x + pandas + python-dotenv
- PostgreSQL
- dbt
- Apache Airflow
- Docker

## Setup
1. Clone the repo
2. Create a virtual environment: `python3 -m venv venv`
3. Activate it: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and fill in your values