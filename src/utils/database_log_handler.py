import logging
from typing import override
from utils.database import Database
from models import Log

session = Database().get_session()

class DatabaseHandler(logging.Handler):
    @override
    def emit(self, record):
        try:
            session.add(Log(
                level = record.levelno,
                url=getattr(record, 'url', None),
                method=getattr(record, 'method', None),
                process_time=getattr(record, 'process_time', None),
                response_code=getattr(record, 'response_code', None),
                user=getattr(record, 'user', None),
                body=getattr(record, 'body', None)
            ))
            session.commit()
        except Exception as e:
            print(e)