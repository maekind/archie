# encoding:utf-8
"""
speaker_recognition.py - File that contains class with speaker recognition methods
"""

import logging
import time
import os
import _pickle as cPickle
import numpy as np
from scipy.io.wavfile import read
from lib.recognition.speaker_features import SpeakerFeatures
import warnings
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

    def __init__(self, model_path) -> None:
        """
        Default constructor
        """
        # Initialize logger name
        self._logger = logging.getLogger("Speaker Recognition")
        # Set model path variable
        self._model_path = model_path
        # TODO: Load models in initialization

    def find_speaker(self, audio_file):
        """
        Method to find best speaker recognition from trainned files
        """
        gmm_files = [os.path.join(self._model_path, fname) for fname in
                     os.listdir(self._model_path) if fname.endswith('.gmm')]

        # Load the Gaussian Models
        models = [cPickle.load(open(fname, 'rb')) for fname in gmm_files]
        speakers = [fname.split("/")[-1].split(".gmm")[0] for fname
                    in gmm_files]

        # Read the test directory and get the list of test audio files
        sr, audio = read(audio_file)
        self._logger.debug(f"Checking speaker in {audio_file} with rate {sr}")
        sf = SpeakerFeatures(audio, sr)
        vector = sf.extract_features()

        log_likelihood = np.zeros(len(models))

        for i in range(len(models)):
            gmm = models[i]  # checking with each model one by one
            scores = np.array(gmm.score(vector))
            log_likelihood[i] = scores.sum()

        winner = np.argmax(log_likelihood)
        self._logger.info(
            f"Detected speaker: {speakers[winner].split('-')[0]}")

        return speakers[winner]
