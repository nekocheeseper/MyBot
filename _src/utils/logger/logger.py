import logging
import datetime
import pathlib

class ColourFormatter(logging.Formatter):
    COLOURS = [
        (logging.DEBUG, '\x1b[40;1m'),
        (logging.INFO, '\x1b[34;1m'),
        (logging.WARNING, '\x1b[33;1m'),
        (logging.ERROR, '\x1b[31m'),
        (logging.CRITICAL, '\x1b[41m'),
    ]
    FORMATS = {
        level: logging.Formatter(f"\x1b[30;1m%(asctime)s\x1b[0m {colour}%(levelname)-8s\x1b[0m \x1b[35m%(name)s\x1b[0m %(message)s", "%Y-%m-%d %H:%M:%S")
        for level, colour in COLOURS
    }
    def format(self, record):
        formatter = self.FORMATS.get(record.levelno)
        if formatter is None:
            formatter = self.FORMATS[logging.DEBUG]
        if record.exc_info:
            text = formatter.formatException(record.exc_info)
            record.exc_text = f"\x1b[31m{text}\x1b[0m"
        output = formatter.format(record)
        record.exc_text = None
        return output
    
class DailyFileHandler(logging.FileHandler):
    def __init__(self, log_dir: str):
        self.log_dir = pathlib.Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.current_date = datetime.datetime.now().date()
        filename = self.log_dir / f"{self.current_date}.log"
        super().__init__(filename, encoding="utf-8")

    def reopen_if_needed(self):
        today = datetime.datetime.now().date()
        if today == self.current_date: return
        if self.stream: self.close()
        self.current_date = today
        self.baseFilename = str(self.log_dir / f"{today}.log")
        self.stream = self._open()

    def emit(self, record):
        try:
            self.reopen_if_needed()
            super().emit(record)
        except Exception:
            self.handleError(record)

log_header = None
daily_file_handler = None
    
def init(base_dir, header):
    global log_header, daily_file_handler
    log_header = header
    daily_file_handler = DailyFileHandler(log_dir = f"{base_dir}/logs/")
    file_handler = daily_file_handler
    file_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)-8s %(name)s %(message)s", "%Y-%m-%d %H:%M:%S"))
    discord_logger = logging.getLogger("discord")
    discord_logger.setLevel(logging.INFO)
    discord_logger.addHandler(file_handler)
    return

class Logger:
    def __init__(self):
        self.logger = None
        return

    def init(self, log_name="log"):
        file_handler = daily_file_handler
        file_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)-8s %(name)s %(message)s", "%Y-%m-%d %H:%M:%S"))
        handler = logging.StreamHandler()
        handler.setFormatter(ColourFormatter())
        self.logger = logging.getLogger(f"{log_header}.{log_name}")
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(handler)
        self.logger.addHandler(file_handler)
        return

    def info(self, context):
        self.logger.info(context)
        return

    def warning(self, context):
        self.logger.warning(context)
        return

    def error(self, context):
        self.logger.error(context)
        return
