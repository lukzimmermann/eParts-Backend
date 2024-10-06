import logging
import sys
from utils.database_log_handler import DatabaseHandler

class LogFilter(logging.Filter):
    def filter(self, record):
        return True
    

logger = logging.getLogger("eParts")

formatter = logging.Formatter(
    fmt = "%(asctime)s - %(levelname)s - %(message)s"
)

stream_handler = logging.StreamHandler(sys.stdout)
file_handler = logging.FileHandler('app.log')
database_handler = DatabaseHandler()

stream_handler.addFilter(LogFilter())
database_handler.addFilter(LogFilter())

stream_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)
database_handler.setFormatter(formatter)

logger.handlers = [stream_handler, file_handler, database_handler]

logger.setLevel(logging.INFO)