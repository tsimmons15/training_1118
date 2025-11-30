import logging
import logging.handlers
import os

def setup_logger(name = "app", log_dir = "log", log_level = logging.INFO, sep = '/', enableConsole=True):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Formatter
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(filename)s:%(lineno)d | %(message)s"
    )

    filename = f"{log_dir}{sep}{name}.log"
    os.makedirs(log_dir, exist_ok=True)


    # File Handler (Rotating files)
    file_handler = logging.handlers.TimedRotatingFileHandler(
        filename=filename, when='midnight', backupCount=5
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    # Console Handler
    if (enableConsole):
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger
