# encoding:utf-8

"""
weather_engine.py - Weather daemon to request for weather forecast
"""

import logging
import time
from config.base import Configuration

class WeatherEngine():
    """
    Class to request for weather forecast
    """

    def __init__(self, root_path) -> None:
        """
        Default constructor
        """
        # Set logger name
        self._logger = logging.getLogger("Weather Engine")

        # Load configuration
        self._logger.info("Loading configuration ...")
        config = Configuration(root_path)
        self._logger.info("ok")

        # Get weather file
        self._weather_file = config.weather.weather_file

        # Get timer
        self._timer = config.weather.timer

    def run(self):
        """
        Function that launches engine
        """
        start_time = time.perf_counter()

        while True:
            # If timer seconds passed
            if time.perf_counter() - start_time > self._timer:
                self._request_weather()
                start_time = time.perf_counter()

            time.sleep(1)

    def _request_weather(self):
        """
        Function to request weather info and save to temp file
        """
        


            


