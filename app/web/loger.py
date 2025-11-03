from logging import getLogger, Formatter, StreamHandler


LONG_LOGGER_FORMAT = "[%(asctime)s.%(msecs)03d] [%(processName)s] %(levelname)s %(module)10s:%(funcName)s:%(lineno)-3d %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
LOGGER_LEVEL = "INFO"


def setup_logger():
    base_logger = getLogger()
    base_logger.setLevel(LOGGER_LEVEL)

    stream_handler = StreamHandler()

    stream_formatter = Formatter(LONG_LOGGER_FORMAT, DATE_FORMAT)
    stream_handler.setFormatter(stream_formatter)

    base_logger.addHandler(stream_handler)

    base_logger.info("Logger added")
