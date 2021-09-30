# encoding:utf-8

"""
step.py - File that contains engine's step class
"""

from enum import Enum


class Step(Enum):
    """
    Enumeration class to define ai engine steps
    """
    # Listening and waiting for the activation token
    LISTENING_NOT_ACTIVE = 1
    # Listening for incoming orders after interaction activated
    LISTENING_ACTIVE = 2
    # Trainning models
    TRAINNING = 3
    # Recognizing speaker's voice
    RECOGNITION = 4
    # Speaking
    SPEAKING = 5
    # Processing input speech
    PROCESSING = 6
