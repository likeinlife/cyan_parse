import logging
from pathlib import Path

MAX_ADS = 50
MAX_ADS_PER_HOUSE = 4
NEEDED_MONTH = ["апр", "май", "июн", "июл", "авг", "сен"]
NEEDED_YEAR = ["2023"]
LOGGING_LEVEL = logging.INFO

CYAN_FILENAME = Path("cyan.csv")
CYAN_TRANSFORMED_FILENAME = Path("cyan-upd.csv")
CYAN_ARCHIVE_FILENAME = Path("cyan-archive.csv")
