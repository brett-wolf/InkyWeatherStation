from datetime import datetime
import logging, traceback
from logging.handlers import RotatingFileHandler

log_formatter = logging.Formatter(
    "%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s"
)

logFile = "/home/evolmonster/InkyWeatherStation/logs/logging.log"

my_handler = RotatingFileHandler(
    logFile, mode="w", maxBytes=5 * 1024 * 1024, backupCount=1, encoding=None, delay=0
)
my_handler.setFormatter(log_formatter)
my_handler.setLevel(logging.INFO)

app_log = logging.getLogger("root")
app_log.setLevel(logging.INFO)

app_log.addHandler(my_handler)


class LoggingHandler(object):
    def handle_exception(exc_message, exc_object=None):
        print(exc_message)
        if exc_object:
            tb_str = "".join(
                traceback.format_exception(None, exc_object, exc_object.__traceback__)
            )
            app_log.error(exc_message + " " + tb_str)
        else:
            app_log.error(exc_message)

    def log_run_complete():
        with open("/home/evolmonster/InkyWeatherStation/logs/lastrun.txt", "w+") as f:
            f.write(str(datetime.now().strftime("%A %d %b %H:%M:%S")))
