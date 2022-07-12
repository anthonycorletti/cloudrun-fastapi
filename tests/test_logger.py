from datetime import datetime
from typing import Any

from cloudrunfastapi.logger import logger


def test_logger(capsys: Any) -> None:
    logger.exception("this is an exception")

    logger.info(
        "testing types",
        extra={
            "string": "string",
            "bytes": b"test",
            "set": {"test", "test2"},
            "time": datetime.now(),
        },
    )

    class MyUnsupportedType:
        def __init__(self, data: str) -> None:
            self.data = data

    logger.info("testing types", extra={"random": MyUnsupportedType("test")})
    out, err = capsys.readouterr()
    assert out == ""
    assert "TypeError: Object of type MyUnsupportedType is not JSON serializable" in err
