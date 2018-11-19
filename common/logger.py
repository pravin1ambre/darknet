import functools
import logging

DEBUG = True


def create_logger():
    """
    Creates a logging object and returns it
    """
    logger = logging.getLogger("app_logger")
    logger.setLevel(logging.INFO)
    # create the logging file handler
    fh = logging.FileHandler("app.log")
    fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(fmt)
    fh.setFormatter(formatter)
    # add handler to logger object
    logger.addHandler(fh)
    return logger


def exception(function):
    """
    A decorator that wraps the passed in function and logs
    exceptions should one occur
    """
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        logger = create_logger()
        try:
            return function(*args, **kwargs)
        except Exception as e:
            # log the exception
            err = "Exception in function {} and stack trace\n{}".format(
                function.__name__,
                str(e))
            logger.exception(err)
            # re-raise the exception
            if DEBUG:
                raise
    return wrapper
