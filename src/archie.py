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


class ArchieSIGINTCatchedException(Exception):
    """ Exception to handler SIGINT """


class ArchieLauncher():
    """
    Archie ASR launcher class
    """

    # Paths
    _data_path = r"/Users/marco/Documents/Proyectos/P017-Assistant/archie"
    _conf_path = r"/Users/marco/Documents/Proyectos/P017-Assistant/archie/src"
    _services_path = r"/Users/marco/Documents/Proyectos/P017-Assistant/archie/src"

    # Setting signal received
    _signal_received = False

    # Instance initialization for spawning services
    _services: SpawnServices = None

    # Initialize configuration instance
    _config: Configuration = None

    def __init__(self, logging_level) -> None:
        """
        Default constructor
        """
        # Configuring logger
        self._configure_logger(logging_level)

        # Creating logger instance
        self._logger = logging.getLogger("Archie")

        # Set signal handler to catch SIGINT
        signal.signal(signal.SIGINT, self._signal_handler)

        # Getting configuration
        self._get_configuration()

        # Launch services
        self._launch_services()

    def _configure_logger(self, level):
        """
        Method to configure logging
        """
        logargs = {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'}

        logargs["level"] = level

        logging.basicConfig(**logargs)

    @trace_info("Loading configuration file ...")
    def _get_configuration(self):
        """
        Function to get configuration instance
        """
        self._config = Configuration(
            self._conf_path, self._data_path, self._services_path)

    @trace_info("Spawining services ...")
    def _launch_services(self):
        """
        Method to launch services
        """
        # Initialize services
        self._services = SpawnServices(self._config)

        # Spawn services
        self._services.run()

        # We wait some seconds to have services running
        import time
        time.sleep(5)

    def run(self):
        """
        Method to launch Archie Engine
        """
        # Launch archie engine forever
        archie = AIEngine(self._config)
        archie.run()

    @trace_info("Stopping services ...")
    def _stop_services(self):
        """
        Method to stop all running services
        """
        if self._services:
            self._services.stop()

    def _signal_handler(self, sig, frame):
        """
        Method to catch ctrl+c signal
        """
        self._logger.warning('Ctrl+C pressed!')
        # Stop all spawned services
        self._stop_services()

        raise ArchieSIGINTCatchedException()


# Initialize archie to use under signal detection
# archie:ArchieASR = None

# def signal_handler(sig, frame):
#         """
#         Method to catch ctrl+c signal
#         """
#         print('Ctrl+C pressed!')
#         # Stop all spawned services
#         if archie:
#             archie.stop_services()
#         sys.exit(1)

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

    try:
        # TODO: Delete lines:
        # Set signal handler to catch SIGINT
        #signal.signal(signal.SIGINT, signal_handler)

        # Archie instance initialization
        archie = ArchieLauncher(args.logging_level)

        # Launching Archie
        archie.run()

    except ArchieSIGINTCatchedException:
        logger = logging.getLogger()
        logger.warning("Exiting program ...")

    except Exception as e:
        if e is not None:
            logger = logging.getLogger()
            logger.error(e)
            if archie:
                archie.stop_services()
    finally:
        sys.exit(0)


if __name__ == "__main__":
    main()
