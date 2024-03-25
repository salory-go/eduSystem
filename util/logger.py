import logging


class UvicornFormatter(logging.Formatter):
    def format(self, record):
        return f"{record.levelname}:     {record.getMessage()}"


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setFormatter(UvicornFormatter())

logger.addHandler(console_handler)
