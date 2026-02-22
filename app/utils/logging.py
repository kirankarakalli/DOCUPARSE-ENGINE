import logging
import os

log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "logs")
os.makedirs(log_dir, exist_ok=True)

logger=logging.getLogger("docParser")
logger.setLevel(logging.INFO)

set_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                                   "%Y-%m-%d %H:%M:%S")


file_handler=logging.FileHandler(os.path.join(log_dir, "app.log"),encoding="utf-8")
file_handler.setFormatter(set_formatter)

console_handler=logging.StreamHandler()
console_handler.setFormatter(set_formatter)

if not logger.hasHandlers():
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
