# encoding:utf-8

"""
archie.py - Application launcher
"""

import logging
import argparse
import sys
import signal
from os import path
from lib.engine.ai_engine import AIEngine
from services.service import SpawnServices
from utils.info import run_info_command, run_version_command, __application__

# Setting application logging level
LOG_LEVEL = "DEBUG"

# Setting signal received
signal_received = False

# Instance for spawning services
services = SpawnServices(path.dirname(__file__))

def signal_handler(sig, frame):
    """
    Method to catch ctrl+c signal
    """
    signal_received = True
    print('Ctrl+C pressed!')
    # Stop all spawned services
    services.stop()
    sys.exit(0)

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

        # Set signal handler to catch SIGINT
        signal.signal(signal.SIGINT, signal_handler)

        # Spawn services
        services.run()

        # Launch archie engine
        archie = AIEngine(path.dirname(__file__))
        archie.run()

    except Exception as e:
        if not signal_received:
            if e is not None:
                logger.error(e)
            if services:
                services.stop()
                
            sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
