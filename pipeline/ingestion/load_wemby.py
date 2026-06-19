import os
import logging
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

RAW_DATA_PATH = Path("pipeline/ingestion/data/wemby_gamelog_raw.csv")
TABLE_NAME = "wemby_gamelog_raw"


def get_db_engine() -> Engine:
    """Create and return a SQLAlchemy engine using credentials from .env.""" 
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    db = os.getenv("POSTGRES_DB", "de_bootcamp")
    user = os.getenv("POSTGRES_USER", "de_user")
    password = os.getenv("POSTGRES_PASSWORD", "de_password")

    connection_string = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"
    engine = create_engine(connection_string)
    logging.info(f"Connected to Postgres: {host}:{port}/{db}")
    return engine


def load_csv(path: Path) -> pd.DataFrame:
    """Load raw CSV into a DataFrame."""
    if not path.exists():
        raise FileNotFoundError(f"Raw data file not found: {path}")
    df = pd.read_csv(path)
    logging.info(f"Loaded {len(df)} rows from {path}")
    return df


def clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Lowercase all column names for Postgres compatibility."""
    df.columns = [col.lower() for col in df.columns]
    return df


def write_to_postgres(df: pd.DataFrame, engine, table_name: str) -> None:
    """Write DataFrame to Postgres, replacing table if it exists."""
    df.to_sql(
        name=table_name,
        con=engine,
        if_exists="replace",
        index=False
    )
    logging.info(f"Written {len(df)} rows to table '{table_name}'")


def verify_load(engine, table_name: str) -> None:
    """Run a quick count query to confirm data landed."""
    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
        count = result.scalar()
        logging.info(f"Verification: {count} rows found in '{table_name}'")


def run_load(csv_path: Path = RAW_DATA_PATH, table_name: str = TABLE_NAME) -> None:
    """Run the full load job: read CSV, clean columns, write to Postgres, verify."""
    engine = get_db_engine()
    df = load_csv(csv_path)
    df = clean_columns(df)
    write_to_postgres(df, engine, table_name)
    verify_load(engine, table_name)

if __name__ == "__main__":
    try:
        run_load()
        logging.info("Load completed successfully")
    except Exception as e:
        logging.error(f"Load failed: {e}")
        raise