# encoding:utf-8

"""
decorators.py - File that contains decorators
"""

import logging
import functools

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
