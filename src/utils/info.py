# encoding:utf-8

"""
info.py - File that contains application information
"""

import argparse
import sys

__application__ = "Archie (ARtificial Centered Human Inteligence Environment)"
__author__ = "Marco Espinosa"
__license__ = "MIT License"
__version__ = "0.1"
__maintainer__ = "Marco Espinosa"
__email__ = "hi@marcoespinosa.es"
__status__ = "Development"

class run_version_command(argparse.Action):
    """ Class to print version """
    def __call__(self, *args, **kwargs):
        print(__version__)
        sys.exit(0)

class run_info_command(argparse.Action):
    """ Class to print application information """
    def __call__(self, *args, **kwargs):
        print(f"*** {__application__} ***")
        print(f"Author: {__author__}")
        print(f"Version: {__version__}")
        print(f"Email: {__email__}")
        print(f"Status: {__status__}")
        print(f"License: {__license__}")
        sys.exit(0)