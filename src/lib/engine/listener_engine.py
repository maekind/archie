# encoding:utf-8
"""
listener_engine.py - File that contains listener class
"""

import speech_recognition as sr
import logging
from lib.constants import MICROPHONE_INDEX

__authors__ = "Marco Espinosa"
__license__ = "MIT License"
__version__ = "1.0"
__maintainer__ = "Marco Espinosa"
__email__ = "hi@marcoespinosa.es"
__status__ = "Development"


class ListenerRecognizerException(Exception):
    """ Custom exception for recognizer """


class ListenerException(Exception):
    """ Custom exception for listener """


class Listener():
    """
    Class to handler the listener
    """

    def __init__(self, language="es-es") -> None:
        """
        Default constructor
        """
        # Initialize logger name
        self._logger = logging.getLogger("Listener Engine")
        self._logger.info("Initializing listener engine ...")
        # Set language
        self._language = language
        # Initialize listener
        self._listener = sr.Recognizer()
        # Set pause threshold
        self._listener.pause_threshold = 1
        # Set microphone adjustment
        self._micro_adjustment = False

        self._logger.info("ok")

    def listen(self) -> str:
        """
        Method to listen. It returns transcription
        """
        query = ""
        try:
            with sr.Microphone(device_index=MICROPHONE_INDEX) as source:
                self._logger.info("Listenning ...")
                # if not self._micro_adjustment:
                #     # Set sensitivity
                #     self._listener.adjust_for_ambient_noise(source)
                #     self._micro_adjustment = True

                audio = self._listener.listen(source)
                self._logger.info("Someone said something!")
        except Exception as e:
            raise ListenerException(f"Unable to open microphone: {e}")

        # try:
        #     self._logger.info("Recognizing ...")
        #     query = self._listener.recognize_google(audio, language=self._language)
        #     self._logger.info(f"Someone said {query}")
        # except Exception as e:
        #     raise ListenerRecognizerException(f"Unable to recognize your voice: {e}")

        return query, audio

# Troubleshooting
# The recognizer tries to recognize speech even when I’m not speaking, or after I’m done speaking.
# Try increasing the recognizer_instance.energy_threshold property. This is basically how sensitive the recognizer is to when recognition should start. Higher values mean that it will be less sensitive, which is useful if you are in a loud room.
# This value depends entirely on your microphone or audio data. There is no one-size-fits-all value, but good values typically range from 50 to 4000.
# Also, check on your microphone volume settings. If it is too sensitive, the microphone may be picking up a lot of ambient noise. If it is too insensitive, the microphone may be rejecting speech as just noise.
# The recognizer can’t recognize speech right after it starts listening for the first time.
# The recognizer_instance.energy_threshold property is probably set to a value that is too high to start off with, and then being adjusted lower automatically by dynamic energy threshold adjustment. Before it is at a good level, the energy
# threshold is so high that speech is just considered ambient noise. The solution is to decrease this threshold, or call recognizer_instance.adjust_for_ambient_noise beforehand, which will set the threshold to a good value automatically.
