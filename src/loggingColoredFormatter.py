import logging


class ColoredFormatter(logging.Formatter):
    grey = "\x1b[38;21m"
    blue = "\x1b[38;5;39m"
    yellow = "\x1b[38;5;226m"
    red = "\x1b[38;5;196m"
    boldRed = "\x1b[31;1m"
    reset = "\x1b[0m"

    def __init__(self, fmt, notifier, verbose_notifs):
        super().__init__()
        self.fmt = fmt
        self.notifier = notifier
        self.verbose_notifs = verbose_notifs
        self.FORMATS = {
            logging.DEBUG: self.grey + self.fmt + self.reset,
            logging.INFO: self.blue + self.fmt + self.reset,
            logging.WARNING: self.yellow + self.fmt + self.reset,
            logging.ERROR: self.red + self.fmt + self.reset,
            logging.CRITICAL: self.boldRed + self.fmt + self.reset,
        }

    def format(self, record):
        logFmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(logFmt)
        if self.verbose_notifs:
            self.notifier.send(f"[{logging.getLevelName(record.levelno)}] {record.msg}")
        return formatter.format(record)
