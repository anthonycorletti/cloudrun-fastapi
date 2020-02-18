import logging
import time


def get_logger():
    tz = time.strftime('%z')
    logging.config = logging.basicConfig(
        format=(f'[%(asctime)s.%(msecs)03d {tz}] '
                '[%(process)s] [%(filename)s L%(lineno)d] '
                '[%(levelname)s] %(message)s'),
        level='INFO',
        datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger(__name__)
    return logger
