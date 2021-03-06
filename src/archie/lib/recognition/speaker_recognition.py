# encoding:utf-8
"""
speaker_recognition.py - File that contains class with speaker recognition methods
"""

import logging
import os
import _pickle as cPickle
import numpy as np
import warnings
from scipy.io.wavfile import read
from archie.lib.recognition.speaker_features import SpeakerFeatures
from archie.utils.decorators import trace_info

warnings.filterwarnings("ignore")

__authors__ = "Marco Espinosa"
__license__ = "MIT License"
__version__ = "1.0"
__maintainer__ = "Marco Espinosa"
__email__ = "hi@marcoespinosa.es"
__status__ = "Development"
__credits__ = ["Abhijeet Kumar",
               "Speaker-identification-using-GMMs", "abhijeet.kumar@fmr.com"]


class SpeakerRecognition():
    """
    Class to recognize speakers
    """

    # List to store trained models. Tuple of (model, speaker name)
    _models = []

    @trace_info("Initializing speaker recognition ...")
    def __init__(self, model_path) -> None:
        """
        Default constructor
        """
        # Initialize logger name
        self._logger = logging.getLogger(self.__class__.__name__)
        # Set model path variable
        self._model_path = model_path
        # Load models in initialization
        self._load_models()

    def __repr__(self) -> str:
        """ Return a printed version """
        return f"{self.__class__.__name__}, models path: {self._model_path}"
        
    def find_speaker(self, audio_file):
        """
        Method to find best speaker recognition from trainned files
        """
        # Read the test directory and get the list of test audio files
        sr, audio = read(audio_file)
        self._logger.debug(f"Checking speaker in {audio_file} with rate {sr}")
        sf = SpeakerFeatures(audio, sr)
        vector = sf.extract_features()

        log_likelihood = np.zeros(len(self._models))

        for i in range(len(self._models)):
            gmm, _ = self._models[i]
            scores = np.array(gmm.score(vector))
            log_likelihood[i] = scores.sum()

        winner = np.argmax(log_likelihood)
        _, speaker = self._models[winner]

        return speaker

    @trace_info("Loading models ...")
    def _load_models(self, force=False):
        """
        Method to load trained models
        """
        gmm_files = [os.path.join(self._model_path, fname) for fname in
                     os.listdir(self._model_path) if fname.endswith('.gmm')]

        # If force, empty list
        if force:
            self._logger.debug("Cleanning models list")
            self._models.clear()

        # Load the Gaussian Models
        for model in gmm_files:
            gmm = cPickle.load(open(model, 'rb'))
            speaker = model.split("/")[-1].split(".gmm")[0].split('-')[0]
            
            self._models.append((gmm, speaker))
            self._logger.debug(f"{speaker} loaded successfully")

    def force_reload(self):
        """
        Method to force reloading files from models path
        """
        self._load_models(force=True)
