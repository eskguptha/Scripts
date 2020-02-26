__author__ = 'Santhosh Emmadi'
"""
https://github.com/eskguptha
"""
import os, sys, logging
from django.conf import settings
from logging import handlers

LOG_ROTATE = 'midnight'
BASE_DIR  = settings.BASE_DIR
formatter = logging.Formatter('[%(asctime)s] %(levelname)s %(message)s')
log_level = logging.DEBUG if settings.DEBUG else logging.INFO

#MODEL LOGGER
LOG_FILE = os.path.join(BASE_DIR, 'logs', 'model.log')
mhandler = handlers.TimedRotatingFileHandler(LOG_FILE, when=LOG_ROTATE)
mhandler.setFormatter(formatter)
mlogger = logging.getLogger("model")
mlogger.addHandler(mhandler)
mlogger.setLevel(log_level)


#rs232 device LOGGER
LOG_FILE = os.path.join(BASE_DIR, 'logs', 'rs232.log')
whandler = handlers.TimedRotatingFileHandler(LOG_FILE, when=LOG_ROTATE)
whandler.setFormatter(formatter)
rs232logger = logging.getLogger("rs232")
rs232logger.addHandler(whandler)
rs232logger.setLevel(log_level)

#lan socket LOGGER
LOG_FILE = os.path.join(BASE_DIR, 'logs', 'lan.log')
lhandler = handlers.TimedRotatingFileHandler(LOG_FILE, when=LOG_ROTATE)
lhandler.setFormatter(formatter)
lanlogger = logging.getLogger("rs232")
lanlogger.addHandler(lhandler)
lanlogger.setLevel(log_level)

#GENERAL Form LOGGER
LOG_FILE = os.path.join(BASE_DIR, 'logs', 'general.log')
ghandler = handlers.TimedRotatingFileHandler(LOG_FILE, when=LOG_ROTATE)
ghandler.setFormatter(formatter)
glogger = logging.getLogger("general")
glogger.addHandler(ghandler)
glogger.setLevel(log_level)


#restapi LOGGER
LOG_FILE = os.path.join(BASE_DIR, 'logs', 'restapi.log')
sahandler = handlers.TimedRotatingFileHandler(LOG_FILE, when=LOG_ROTATE)
sahandler.setFormatter(formatter)
restlogger = logging.getLogger("restapi")
restlogger.addHandler(sahandler)
restlogger.setLevel(log_level)
