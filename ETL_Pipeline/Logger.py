import logging

class ColorFormatter(logging.Formatter):
    gray = '\x1b[38;5;239m'
    blue = '\x1b[1;34m'
    yellow = '\x1b[38;5;221m'
    red = '\x1b[31;20m'
    intense_red = '\x1b[31;1m'
    reset = '\x1b[0m'

    log_format = '%(levelname)s -- %(name)s: %(message)s'

    Formats = {
        logging.DEBUG: gray + log_format + reset,
        logging.INFO: blue + log_format + reset,
        logging.WARNING: yellow + log_format + reset,
        logging.ERROR: red + log_format + reset,
        logging.CRITICAL: intense_red + log_format + reset
    }

    def format(self, record):
        log_fmt = self.Formats.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)