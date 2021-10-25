# encoding:utf-8

"""
services.py - File that contains Service class to spawn services
"""

import subprocess
import logging
import signal
from os import path
from collections import deque
from config.base import Configuration


class SpawnServices():
    """
    Class to spawn services
    """

    def __init__(self, root_path) -> None:
        """
        Default constructor
        """
        # Set logger name
        self._logger = logging.getLogger("Spawn Services")

        # Load configuration
        self._logger.info("Loading services configuration ...")
        config = Configuration(root_path)
        self._logger.info("ok")

        # Load python executable
        self._python_exe = config.services.python_exe

        # Load services path
        self._services_path = config.services.path

        # Load list of available services
        self._services = config.services.services

        # Initialize spawned services list
        self._spawned_services = deque([])

        # Initialize service main file name
        self._service_main_file = "service.py"

    def run(self):
        """"
        Method to launch spawn function
        """
        for service in self._services:
            self._spawn_service(service)

    def stop(self):
        """
        Method to stop spawned services
        """
        services = self._spawned_services

        for process, service in services:
            try:
                # Send CTRL+c to kill the child process from su -
                self._logger.warning(f"Sending stop signal to {service}...")
                process.send_signal(signal.SIGINT)
                self._logger.info(f"{service} stopped")
                
            except subprocess.TimeoutExpired:
                self._logger.error(f"Stopping service {service} timeout!")
                process.kill()
            
            self._spawned_services.remove((process, service))

    def _spawn_service(self, service):
        """
        Method to spawn services
        """
        self._logger.info(f"Spawning service {service} ...")
        # Launching service
        spawned = subprocess.Popen([self._python_exe, path.join(
            self._services_path, service, self._service_main_file)])
        # Save service handler to spawned services list
        self._spawned_services.append((spawned, service))
        self._logger.info("ok")

    