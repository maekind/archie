# encoding:utf-8

"""
archie.py - Application launcher
"""

import logging
import argparse
import sys
import signal
from os import path
from archie.lib.engine.ai_engine import AIEngine
from archie.services.spawn import SpawnServices
from archie.utils.info import run_info_command, run_version_command, __application__
from archie.config.base import Configuration
from archie.utils.decorators import trace_info

# Paths
data_path = r"/Users/marco/Documents/Proyectos/P017-Assistant/archie"
conf_path = r"/Users/marco/Documents/Proyectos/P017-Assistant/archie/src"
services_path = r"/Users/marco/Documents/Proyectos/P017-Assistant/archie/src"

# Setting signal received
signal_received = False

# Instance initialization for spawning services
services = None

def signal_handler(sig, frame):
    """
    Method to catch ctrl+c signal
    """
    signal_received = True
    print('Ctrl+C pressed!')
    # Stop all spawned services
    if services:
        services.stop()
    sys.exit(0)

def configure_logger(level):
    """
    Method to configure logging
    """
    logargs = {
        'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        'datefmt': '%Y-%m-%d %H:%M:%S'}

    logargs["level"] = level

    logging.basicConfig(**logargs)

    return logging.getLogger("Archie")

@trace_info("Loading configuration file ...")
def get_configuration():
    """
    Function to get configuration instance
    """
    return Configuration(conf_path, data_path, services_path)


def main():
    """
    Main function
    """
    
    # Configure arguments
    parser = argparse.ArgumentParser(description=__application__)
    parser.add_argument('--version', nargs=0,
                        help=argparse.SUPPRESS, action=run_version_command)
    parser.add_argument('-i', '--info', nargs=0,
                        help="show application information", action=run_info_command)
    parser.add_argument('-l', 
                        '--logging_level',
                        default='DEBUG',
                        help="set logging level to one of the following values: [DEBUG, INFO, WARNING, ERROR, CRITICAL]")

    args = parser.parse_args()

    # Configure logger
    logger = configure_logger(args.logging_level)
    logger.info(f"Set logging level to {args.logging_level}")

    try:
        
        # Set signal handler to catch SIGINT
        signal.signal(signal.SIGINT, signal_handler)

        # Get configuration instance
        config = get_configuration()

        # Initialize services
        services = SpawnServices(config)

        # Spawn services
        services.run()

        # We wait some seconds to have services running
        import time
        time.sleep(5)
        
        # Launch archie engine
        archie = AIEngine(config)
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
