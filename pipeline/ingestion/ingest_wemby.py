import time
import logging
import pandas as pd
from pathlib import Path
from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

PLAYER_NAME = "Victor Wembanyama"
SEASON = "2024-25"
OUTPUT_PATH = Path("pipeline/ingestion/data/wemby_gamelog_raw.csv")


def get_player_id(name: str) -> int:
    """Look up a player's NBA.com ID by full name."""
    results = players.find_players_by_full_name(name)
    if not results:
        raise ValueError(f"Player not found: {name}")
    player_id = results[0]["id"]
    logging.info(f"Found player: {name} (ID: {player_id})")
    return player_id


def fetch_gamelog(player_id: int, season: str) -> pd.DataFrame:
    """Fetch full season game log for a player from NBA.com."""
    logging.info(f"Fetching game log for player {player_id}, season {season}")
    time.sleep(1)  # NBA.com limits aggressive requests
    gamelog = playergamelog.PlayerGameLog(
        player_id=str(player_id),
        season=season
    )
    df = gamelog.get_data_frames()[0]
    logging.info(f"Fetched {len(df)} games")
    return df


def save_raw(df: pd.DataFrame, path: Path) -> None:
    """Save raw DataFrame to CSV without any transformation."""
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    logging.info(f"Raw data saved to {path}")


if __name__ == "__main__":
    try:
        player_id = get_player_id(PLAYER_NAME)
        df = fetch_gamelog(player_id, SEASON)
        save_raw(df, OUTPUT_PATH)
        logging.info("Ingestion completed successfully")
    except Exception as e:
        logging.error(f"Ingestion failed: {e}")
        raise