# encoding:utf-8

"""
spawn.py - File that contains class to spawn services
"""

import subprocess
import logging
import signal
from os import path
from collections import deque
from archie.utils.decorators import trace_info
from archie.config.base import Configuration


class SpawnServices():
    """
    Class to spawn services
    """

    def __init__(self, config:Configuration) -> None:
        """
        Default constructor
        """
        # Set logger name
        self._logger = logging.getLogger("SpawnServices")

        # Set config instance
        self._config = config
        
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
    
    def __repr__(self) -> str:
        """ Return a printed version """
        return f"{self.__class__.__name__}, services path: {self._services_path}"

    def run(self):
        """"
        Method to launch spawn function
        """
        for service, config in self._services.items():
            if config.get("enabled"):
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
