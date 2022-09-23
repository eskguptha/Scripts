""" 
Creating the Loggers 
"""
import logging
import os
from datetime import date
from logging import handlers

LOG_ROTATE = 'midnight'
BASE_DIR = os.getcwd()
LOG_FORMATTER = logging.Formatter('[%(asctime)s] %(levelname)s %(message)s')
LOG_LEVEL = logging.DEBUG
LOG_ROTATE = 'midnight'

# create a logs' directory if not already exists
try:
    os.makedirs(os.path.join(BASE_DIR, "logs"))
except FileExistsError:
    pass

def getAppLogger(name):
    LOG_FILE = os.path.join(BASE_DIR, 'logs', '{}_{}.log'.format(name, date.today().strftime("%Y-%B-%d")))
    handler = handlers.TimedRotatingFileHandler(LOG_FILE, when=LOG_ROTATE)
    handler.setFormatter(LOG_FORMATTER)
    logger = logging.getLogger(str(name))
    logger.addHandler(handler)
    logger.setLevel(LOG_LEVEL)
    return logger

# #ap_scheduler LOGGER
# LOG_FILE = os.path.join(BASE_DIR, 'logs', 'ap_scheduler.log')
# ahandler = handlers.TimedRotatingFileHandler(LOG_FILE, when=LOG_ROTATE)
# ahandler.setFormatter(LOG_FORMATTER)
# apscheduler_logger = logging.getLogger("apscheduler")
# apscheduler_logger.addHandler(ahandler)
# apscheduler_logger.setLevel(LOG_LEVEL)

# #GENERAL LOGGER
# LOG_FILE = os.path.join(BASE_DIR, 'logs', 'general.log')
# ghandler = handlers.TimedRotatingFileHandler(LOG_FILE, when=LOG_ROTATE)
# ghandler.setFormatter(formatter)
# glogger = logging.getLogger("general")
# glogger.addHandler(ghandler)
# glogger.setLevel(log_level)

glogger = getAppLogger('general')
apscheduler_logger = getAppLogger('apscheduler')
