import pandas as pd
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def load_data(path: Path) -> pd.DataFrame:
    """Load CSV from path and return a DataFrame."""
    if not path.exists():
        logging.error(f"Input file not found: {path}")
        raise FileNotFoundError(f"Input file not found: {path}")
    logging.info(f"Loading data from {path}")
    df = pd.read_csv(path)
    logging.info(f"Loaded {len(df)} rows")
    return df
    
def transform(df: pd.DataFrame) -> pd.DataFrame:
    """Add a revenue column and aggregate by country."""
    df["revenue"] = df["quantity"] * df["unit_price"]
    summary = (
        df.groupby("country")["revenue"]
        .sum()
        .reset_index()
        .rename(columns={"revenue": "total_revenue"})
        .sort_values("total_revenue", ascending=False)
    )
    return summary

def write_output(df: pd.DataFrame, path: Path) -> None:
    """Write DataFrame to CSV."""
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    logging.info(f"Output written to {path}")
if __name__ == "__main__":
    input_path = Path("week1/data/sales.csv")
    output_path = Path("week1/data/sales_summary.csv")

    try:
        df = load_data(input_path)
        summary = transform(df)
        write_output(summary, output_path)
        logging.info("Pipeline completed successfully")
    except FileNotFoundError as e:
        logging.error(f"Pipeline failed: {e}")