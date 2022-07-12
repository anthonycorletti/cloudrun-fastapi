import datetime
import json
import logging
import os
import socket
from typing import Any


class LogEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, bytes):
            return obj.decode("utf-8")
        elif isinstance(obj, (set, frozenset)):
            return tuple(obj)
        elif isinstance(obj, (datetime.datetime, datetime.date, datetime.time)):
            return obj.isoformat()
        return super().default(obj)


class StructuredMessage:
    def __init__(self, **kwargs: Any) -> None:
        self.kwargs = kwargs

    def __str__(self) -> str:
        return LogEncoder().encode(self.kwargs)


class OnelineFormatter(logging.Formatter):
    def formatException(self, exc_info: Any) -> str:
        result = super().formatException(exc_info)
        return repr(result)

    def format(self, record: logging.LogRecord) -> str:
        result = super().format(record)
        if record.exc_text:
            result = result.replace("\n", "")
        result_dict = record.__dict__
        result_dict["host"] = socket.gethostname()
        return str(StructuredMessage(**result_dict))


class StructuredLogger:
    DEFAULT_LEVEL = "INFO"

    @staticmethod
    def create_logger() -> logging.Logger:
        logger = logging.getLogger(__name__)
        log_handler = logging.StreamHandler()
        formatter = OnelineFormatter(datefmt="%Y-%m-%d %H:%M:%S")
        log_handler.setFormatter(formatter)
        logger.addHandler(log_handler)
        logger.setLevel(os.getenv("LOG_LEVEL", StructuredLogger.DEFAULT_LEVEL).upper())
        return logger


logger = StructuredLogger.create_logger()
