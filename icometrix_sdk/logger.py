import logging

# https://docs.python.org/3/howto/logging.html#configuring-logging-for-a-library

logger_name = 'icometrix-sdk'
logging.getLogger(logger_name).addHandler(logging.NullHandler())
