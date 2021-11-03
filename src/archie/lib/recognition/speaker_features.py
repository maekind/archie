# encoding:utf-8

"""
speaker_features.py - This file contains class with methods to extract speech features
from an audio
"""

import logging
import numpy as np
import python_speech_features as mfcc
from sklearn import preprocessing

__authors__ = "Marco Espinosa"
__license__ = "MIT License"
__version__ = "1.0"
__maintainer__ = "Marco Espinosa"
__email__ = "hi@marcoespinosa.es"
__status__ = "Development"
__credits__ = ["Abhijeet Kumar",
               "Speaker-identification-using-GMMs", "abhijeet.kumar@fmr.com"]


class SpeakerFeatures():
    """
    Class to handler auxiliar methods to extract
    speech features using method MFCC + delta
    @Note :  20 dim MFCC(19 mfcc coeff + 1 frame log energy)
    20 dim delta computation on MFCC features. 
    """

    def __init__(self, audio, rate) -> None:
        """
        Default constructor
        """
        # Set audio variable
        self._audio = audio
        # Set rate variable
        self._rate = rate
        # Initialize logger
        self._logger = logging.getLogger("Speaker Features")

    def _calculate_delta(self, array):
        """
        Calculate and returns the delta of given feature vector matrix
        """

        rows, cols = array.shape
        deltas = np.zeros((rows, 20))
        N = 2
        for i in range(rows):
            index = []
            j = 1
            while j <= N:
                if i-j < 0:
                    first = 0
                else:
                    first = i-j
                if i+j > rows - 1:
                    second = rows - 1
                else:
                    second = i+j
                index.append((second, first))
                j += 1
            deltas[i] = (array[index[0][0]]-array[index[0][1]] +
                         (2 * (array[index[1][0]]-array[index[1][1]]))) / 10
        return deltas

    def extract_features(self):
        """
        Extract 20 dim mfcc features from an audio, performs CMS and combines 
        delta to make it 40 dim feature vector
        """

        mfcc_feat = mfcc.mfcc(self._audio, self._rate,
                              0.025, 0.01, 20, nfft=512, appendEnergy=True)

        mfcc_feat = preprocessing.scale(mfcc_feat)
        delta = self._calculate_delta(mfcc_feat)
        combined = np.hstack((mfcc_feat, delta))

        return combined
