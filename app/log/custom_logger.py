import os
import re
import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from datetime import datetime

from app.config.settings import settings


class NoUpdateDifferenceFilter(logging.Filter):
    FILTER_MESSAGES = {
        "message is not modified: specified new message content and reply markup are exactly the same as a current content and reply markup of the message"
    }
    FILTER_REGEX = re.compile("-".join(re.escape(msg) for msg in FILTER_MESSAGES))

    def filter(self, record):
        message = record.getMessage()
        return not self.FILTER_REGEX.search(message)


class ColoredFormatter(logging.Formatter):
    RESET = "\x1b[0m"
    TIME_COLOR = "\x1b[36;1m"
    WHITE = "\x1b[37;1m"
    MSG_COLOR = "\x1b[34;1m"
    COLORS = {
        'DEBUG': "\x1b[36;1m",
        'INFO': "\x1b[32;1m",
        'WARNING': "\x1b[33;1m",
        'ERROR': "\x1b[31;1m",
        'CRITICAL': "\x1b[1;41m"
    }

    def format(self, record):
        record_dict = record.__dict__.copy()
        record_dict['colon'] = f"{self.WHITE}:{self.RESET}"
        record_dict['lineno'] = f"{self.WHITE}{record.lineno}{self.RESET}"
        record_dict['filename'] = f"{self.WHITE}{record.filename}{self.RESET}"
        record_dict['asctime'] = f"{self.TIME_COLOR}{self.formatTime(record, self.datefmt)}{self.RESET}"
        record_dict['name'] = f"{self.WHITE}{record.name}{self.RESET}"
        record_dict['levelname'] = f"{self.COLORS.get(record.levelname, self.RESET)}{record.levelname}{self.RESET}"
        record_dict['message'] = f"{self.MSG_COLOR}{record.getMessage()}{self.RESET}"
        log_format = self._fmt
        return log_format % record_dict


def setup_logging(level=logging.INFO, datefmt='%d.%m.%Y %H:%M:%S'):
    # Конвертер времени для часового пояса Europe/Moscow
    logging.Formatter.converter = lambda *args: datetime.now(tz=settings.DEFAULT_TZ).timetuple()
    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.setLevel(level)

    filter_instance = NoUpdateDifferenceFilter()

    # Настройка консольного обработчика
    console_handler = logging.StreamHandler()
    console_formatter = ColoredFormatter(fmt='%(asctime)s | %(name)s | %(filename)s%(colon)s%(lineno)s | %(levelname)s - %(message)s',
                                         datefmt=datefmt)
    console_handler.setFormatter(console_formatter)
    console_handler.addFilter(filter_instance)
    root_logger.addHandler(console_handler)
    root_logger.info(f"Логирование запущено в {datetime.now(tz=settings.DEFAULT_TZ).isoformat()}")

    # Настройка ротации логов в файл
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    log_file_path = os.path.join(log_dir, "log.txt")
    plain_formatter = logging.Formatter(fmt='%(asctime)s | %(name)s | %(filename)s:%(lineno)s | %(levelname)s - %(message)s',
                                        datefmt=datefmt)
    rotating_handler = TimedRotatingFileHandler(filename=log_file_path, when='midnight',interval=1,
                                                backupCount=60, encoding='utf-8', utc=False)
    rotating_handler.suffix = "%d_%m_%Y"
    rotating_handler.setFormatter(plain_formatter)
    rotating_handler.addFilter(filter_instance)
    root_logger.addHandler(rotating_handler)
