# -*- coding: utf-8 -*-

"""
info.py - Handler for info data in configuration file
"""


class Info():
    """
    Class to hadle info initialization from config file
    """

    def __init__(self, data):
        """
        Default constructor
        """
        self._version = data["version"]
        self._author = data["author"]
        self._license = data["license"]
        self._file = data["file"]
        self._description = data["description"]

    def __repr__(self):
        """
        Return a printed version
        """
        return "%s(version=%r, author=%r, license=%r, file=%r, description=%r)" % (
            self.__class__.__name__, self._version, self._author, self._license, self._file, self._description)

    @property
    def version(self):
        """
        Return version
        """
        return self._version

    @property
    def author(self):
        """
        Return author
        """
        return self._author

    @property
    def license(self):
        """
        Return license
        """
        return self._license

    @property
    def file(self):
        """
        Return file
        """
        return self._file

    @property
    def description(self):
        """
        Return description
        """
        return self._description
