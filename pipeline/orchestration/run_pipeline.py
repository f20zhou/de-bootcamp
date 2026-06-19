import logging
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent / "ingestion"))

from ingest_wemby import run_ingestion
from load_wemby import run_load

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def run_pipeline() -> None:
    """Run the full pipeline: ingest from API, then load into Postgres."""
    logging.info("=== Pipeline started ===")

    logging.info("--- Step 1: Ingestion ---")
    run_ingestion()

    logging.info("--- Step 2: Load to Postgres ---")
    run_load()

    logging.info("=== Pipeline completed successfully ===")


if __name__ == "__main__":
    try:
        run_pipeline()
    except Exception as e:
        logging.error(f"Pipeline failed: {e}")
        sys.exit(1)