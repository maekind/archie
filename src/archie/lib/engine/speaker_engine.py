# encoding:utf-8
"""
speaker_engine.py - File that contains speaker class
"""

import pyttsx3
import logging
from archie.utils.decorators import trace_info

__authors__ = "Marco Espinosa"
__license__ = "MIT License"
__version__ = "1.0"
__maintainer__ = "Marco Espinosa"
__email__ = "hi@marcoespinosa.es"
__status__ = "Development"


class SpeakerVoiceException(Exception):
    """ Custom exception for voice manipulation """
    def __repr__(self) -> str:
        """ Return a printed version """
        return f"{self.__class__.__name__}"

class SpeakerVolumeException(Exception):
    """ Custom exception for volume manipulation """
    def __repr__(self) -> str:
        """ Return a printed version """
        return f"{self.__class__.__name__}"

class Speaker():
    """
    Class to handler the speaker
    """

    @trace_info("Initializing speaker engine ...")
    def __init__(self, language, rate=50, gender='VoiceGenderFemale') -> None:
        """
        Default constructor
        """
        # Initialize logger name
        self._logger = logging.getLogger(self.__class__.__name__)
        
        # Initialize speaker engine
        self._speaker_engine = pyttsx3.init()
        # Set language
        self._language = language
        # Set rate
        self._rate = rate
        # Set geneder
        self._gender = gender
        # Trying to configure speaker voice
        try:
            self._configure_voice()
        except SpeakerVoiceException as e:
            raise e

    def __repr__(self) -> str:
        """ Return a printed version """
        return f"{self.__class__.__name__}, language: {self._language}, rate: {self._rate}, gender: {self._gender}"

    def _configure_voice(self):
        """
        Method to configure speaker voice
        """
        for voice in self._speaker_engine.getProperty('voices'):
            if self._language in voice.languages and self._gender == voice.gender:
                self._speaker_engine.setProperty('voice', voice.id)
                self._speaker_engine.setProperty('rate', self._rate)
                gender = "Female" if "Female" in self._gender else "Male"
                self._logger.info(
                    f"Speaker voice type set to {gender} with a rate of {self._rate} in language {self._language}")
                self._logger.info(f"Volumen level: {self._speaker_engine.getProperty('volume')}")
                return True

        raise SpeakerVoiceException(
            "Language '{}' for gender '{}' not found".format(self._language, self._gender))

    def volume_up(self):
        """
        Method to turn up the speaker volume
        """
        try:
            self._speaker_engine.setProperty(
                'volume', self._speaker_engine.getProperty('volume') + 1)
            self._logger.info(
                f"Volume set to {self._speaker_engine.getProperty('volume')}")
        except Exception as e:
            raise SpeakerVolumeException(f"Volume cannot be modified: {e}")

    def volume_down(self):
        """
        Method to lower the volume
        """
        try:
            self._speaker_engine.setProperty(
                'volume', self._speaker_engine.getProperty('volume') - 1)
            self._logger.info(
                f"Volume set to {self._speaker_engine.getProperty('volume')}")
        except Exception as e:
            raise SpeakerVolumeException(f"Volume cannot be modified: {e}")

    def say(self, something):
        """
        Method to say some thing
        """
        self._speaker_engine.say(something)
        self._speaker_engine.runAndWait()
