# encoding:utf-8
"""
speaker_engine.py - File that contains speaker class
"""

import pyttsx3
import logging
from enum import Enum
from gtts import gTTS
from io import BytesIO
from playsound import playsound
from archie.utils.decorators import trace_info

__authors__ = "Marco Espinosa"
__license__ = "MIT License"
__version__ = "1.0"
__maintainer__ = "Marco Espinosa"
__email__ = "hi@marcoespinosa.es"
__status__ = "Development"

class SpeakerEngine(str, Enum):
    """
    Enumeration class to define speaker engine types
    """
    GTTS = 'gTTS'
    PYTTSX3 = 'pyttsx3'


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

class SpeakerEngineNotFoundException(Exception):
    """ Custom exception for speaker engine not found """
    def __repr__(self) -> str:
        """ Return a printed version """
        return f"{self.__class__.__name__}"

class Speaker():
    """
    Class to handler the speaker
    """

    @trace_info("Initializing speaker engine ...")
    def __init__(self, engine, language, rate=50, gender='VoiceGenderFemale') -> None:
        """
        Default constructor
        """
        # Initialize logger name
        self._logger = logging.getLogger(self.__class__.__name__)
        
        # Set language
        self._language = language
        # Set rate
        self._rate = rate
        # Set geneder
        self._gender = gender
        # Set engine
        self._engine = engine

        # Load desired engine
        self._load_engine()

    @classmethod
    def init_pyttsx3_engine(cls, language, rate=50, gender='VoiceGenderFemale'):
        """
        Constructor to build the pyttsx3 engine
        """
        return cls(SpeakerEngine.PYTTSX3, language, rate, gender)

    @classmethod
    def init_gTTS_engine(cls, language):
        """
        Constructor to build the google gTTS engine
        """
        return cls(SpeakerEngine.GTTS, language)

    def __repr__(self) -> str:
        """ 
        Return a printed version 
        """
        return f"{self.__class__.__name__}, language: {self._language}, rate: {self._rate}, gender: {self._gender}"

    def _load_engine(self):
        """
        Method to load desired engine
        """
        if self._engine == SpeakerEngine.PYTTSX3:
            self._init_pyttsx3_engine()
        elif self._engine == SpeakerEngine.GTTS:
            self._init_gTTS_engine()
        else:
            raise SpeakerEngineNotFoundException()

    @trace_info("Loading pysttsx3 Speaker Engine ...")
    def _init_pyttsx3_engine(self):
        """
        Method to initialize pyttsx3 engine
        """
        # Initialize speaker engine
        self._speaker_engine = pyttsx3.init()
        
        # Trying to configure speaker voice
        try:
            self._configure_voice()
        except SpeakerVoiceException as e:
            raise e

    @trace_info("Loading gTTS Speaker Engine ...")
    def _init_gTTS_engine(self):
        """
        Method to initialize gTTS engine
        """
        # Getting first element. For instance, "es" from "es_ES" string.
        self._language = self._language.split('_')[0]

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
        # pyttsx3 engine
        if self._engine == SpeakerEngine.PYTTSX3:
            self._speaker_engine.say(something)
            self._speaker_engine.runAndWait()
        # gTTS engine
        elif self._engine == SpeakerEngine.GTTS:
            #mp3_fp = BytesIO()
            tts = gTTS(something, lang=self._language)
            #tts.write_to_fp(mp3_fp)
            import tempfile

            temp = tempfile.NamedTemporaryFile(suffix='.mp3', delete=False)
            with open(temp.name, "wb") as mp3_file:
                tts.write_to_fp(mp3_file)
            
            playsound(temp.name)
            # TODO: remove file
                
                


