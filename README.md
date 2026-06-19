# DE Bootcamp Portfolio

End-to-end data engineering pipeline tracking Victor Wembanyama's game-by-game NBA stats.

## Pipeline Architecture
NBA.com (via nba_api) → Python ingestion → Postgres → dbt (coming Week 2) → Airflow (coming Week 3)


## Stack
- Python 3.x, pandas, nba_api, python-dotenv
- PostgreSQL, SQLAlchemy, psycopg2
- dbt (upcoming)
- Apache Airflow (upcoming)
- Docker (upcoming)

## Project Structure
pipeline/ingestion/        # pulls data from NBA.com, loads into Postgres
pipeline/orchestration/    # runs the full pipeline end to end
dbt_project/models/        # dbt transformation models (Week 2+)
week1/                     # early learning exercises, not part of final pipeline

## Setup
1. Clone the repo
2. Create a virtual environment: `python3 -m venv venv`
3. Activate it: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and fill in your Postgres credentials
6. Start Postgres: `sudo service postgresql start`
7. Run the full pipeline: `python3 pipeline/orchestration/run_pipeline.py`