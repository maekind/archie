# encoding:utf-8

"""
archie.py - Application launcher
"""

import logging
import argparse
import sys
from os import path
from lib.engine.ai_engine import AIEngine
from utils.info import run_info_command, run_version_command, __application__

# Setting application logging level
LOG_LEVEL = "DEBUG"


def configure_logger():
    """
    Method to configure logging
    """
    logargs = {
        'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        'datefmt': '%Y-%m-%d %H:%M:%S'}

    logargs["level"] = LOG_LEVEL

    logging.basicConfig(**logargs)

    return logging.getLogger("Archie")


def main():
    """
    Main function
    """
    # Configure logger
    logger = configure_logger()

    # Configure arguments
    parser = argparse.ArgumentParser(description=__application__)
    parser.add_argument('--version', nargs=0,
                        help=argparse.SUPPRESS, action=run_version_command)
    parser.add_argument('-i', '--info', nargs=0,
                        help="show application information", action=run_info_command)

    args = parser.parse_args()

    try:
        archie = AIEngine(path.dirname(__file__))
        archie.run()
    except Exception as e:
        logger.error(e)
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
