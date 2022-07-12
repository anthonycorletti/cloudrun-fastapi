from cloudrunfastapi.logger import logger


def test_logger() -> None:
    logger.exception("this is an exception")
