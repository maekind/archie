# encoding:utf-8
"""
show_microphones.py - File that contains code to find installed microphones
"""

import logging
import speech_recognition as sr

__authors__ = "Marco Espinosa"
__license__ = "MIT License"
__version__ = "1.0"
__maintainer__ = "Marco Espinosa"
__email__ = "hi@marcoespinosa.es"
__status__ = "Production"

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

    return logging.getLogger("Show Microphones util")


def main():
    """ Main fucntion """

    # Configure logger
    logger = configure_logger()

    # Check for micrphones:
    logger.info("Checking for installed microphones ...")
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        logger.info(
            f"Microphone with name \"{name}\" found (device_index={index})")


if __name__ == "__main__":
    main()
