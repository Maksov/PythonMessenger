import logging
from functools import wraps
from logging.handlers import TimedRotatingFileHandler


def configlogging(isserver: bool):
    fmt = '%(asctime)s %(levelname)s %(message)s'
    if isserver:
        filename = './LOG/app.server.log'
        formatter = logging.Formatter(fmt)
        handler = TimedRotatingFileHandler(filename, when="midnight", interval=1)
        handler.suffix = '%Y-%m-%d'
        handler.setFormatter(formatter)
        logger = logging.getLogger('app.server')
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        return logger
    else:
        filename = './LOG/app.client.log'
        loggername = 'app.client'
        logging.basicConfig(
            format=fmt,
            filename=filename,
            level=logging.INFO,
        )
        return logging.getLogger(loggername)


def log(logger):
    def decorator(func):
        @wraps(func)
        def call(*args, **kwargs):
            logger.info('%s %s: Function called', func.__module__, func.__name__)
            try:
                return func(*args, **kwargs)
            except:
                logger.exception('%s %s: Exception: ', func.__module__, func.__name__)
                raise

        return call
    return decorator
