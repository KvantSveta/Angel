import logging


class Logger:
    def __init__(self, file_name="temp.log"):
        file_handler = logging.FileHandler(file_name, "a")
        formatter = logging.Formatter(
            fmt="%(asctime)s %(levelname)s %(message)s",
            datefmt="%e %b %y %H:%M:%S"
        )
        file_handler.setFormatter(fmt=formatter)
        self.logger = logging.getLogger()
        self.logger.addHandler(file_handler)
        self.logger.setLevel(logging.INFO)

    def info(self, msg):
        self.logger.info(msg=msg)

    def error(self, msg):
        self.logger.error(msg=msg)

    def critical(self, msg):
        self.logger.critical(msg=msg)
