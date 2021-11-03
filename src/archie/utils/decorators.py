# encoding:utf-8

"""
decorators.py - File that contains decorators
"""

import logging
import functools
import time


def trace_info(message):
    """ trace logging info decorator """
    def decorator(func):
        """ decorator for function """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            """ wrapper for the decorator """
            logger = logging.getLogger(str(func.__qualname__).split('.')[0])
            logger.info(f"{message}")
            res = func(*args, **kwargs)
            logger.info("ok")
            return res
        return wrapper
    return decorator


def execution_time(func):
    """ calculates function time execution """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        """ decorator wrapper """
        start_time = time.time()
        res = func(*args, **kwargs)
        end_time = time.time()

        logger = logging.getLogger(str(func.__qualname__).split('.')[0])
        logger.info(
            f"Method Name - {func.__name__}, Args - {args}, Kwargs - {kwargs}, Execution Time - {end_time - start_time}")

        return res
    return wrapper
