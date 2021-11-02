# encoding:utf-8

"""
spawn.py - File that contains class to spawn services
"""

import subprocess
import logging
import signal
from os import path
from collections import deque
from utils.decorators import trace_info
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
        self._logger = logging.getLogger("SpawnServices")

        # Load configuration
        self._get_configuration(root_path)

        # Load python executable
        self._python_exe = self._config.services.python_exe

        # Load services path
        self._services_path = self._config.services.path

        # Load list of available services
        self._services = self._config.services.services

        # Initialize spawned services list
        self._spawned_services = deque([])

        # Initialize service main file name
        self._service_main_file = "service.py"

    def run(self):
        """"
        Method to launch spawn function
        """
        for service, config in self._services.items():
            self._spawn_service(service, config)

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

    @trace_info("Loading configuration ...")
    def _get_configuration(self, root_path):
        """
        Method to load configuration
        """
        self._config = Configuration(root_path)

    def _spawn_service(self, service, config):
        """
        Method to spawn services
        """
        self._logger.info(f"Spawning service {service} ...")
        # Launching service
        spawned = subprocess.Popen([self._python_exe, path.join(
            self._services_path, service, self._service_main_file),
            "--host", config.get("host"),
            "--port", str(config.get("port"))])
        # Save service handler to spawned services list
        self._spawned_services.append((spawned, service))
        self._logger.info("ok")
