# encoding:utf-8
"""
statistics.py - File that contains database statistics interface
"""

from abc import ABC
from datetime import datetime
from os import path
from archie.utils.database import Database


class InsertingStatsInDatabaseException(Exception):
    """ Custom exception to handler an exception inserting into the database """
    def __repr__(self) -> str:
        """ Return a printed version """
        return f"{self.__class__.__name__}"

class FetchingStatsInDatabaseException(Exception):
    """ Custom exception to handler an exception fetching data from the database """
    def __repr__(self) -> str:
        """ Return a printed version """
        return f"{self.__class__.__name__}"

class Stats(ABC):
    """
    Main class that implement common elements for statistics
    """
    def __init__(self, db_path, db_name) -> None:
        """
        Default constructor
        """
        self._database = Database(path.join(db_path, db_name))

class SpeechToTextStats(Stats):
    """
    Class that implements speech to text statistics interface
    """
    _TABLE = "speech_to_text"

    def __init__(self, db_path, db_name) -> None:
        """
        Default constructor
        """
        # Call super init function
        super().__init__(db_path, db_name)

    def __repr__(self) -> str:
        """ Return a printed version """
        return f"{self.__class__.__name__}, database: {self._database}"

    def update(self, query):
        """
        Overrides update method
        """

        now = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        day = datetime.now().day
        month = datetime.now().month
        year = datetime.now().year

        if not self._database.insert(self._TABLE, f"'{now}', {day}, {month}, {year}, '{query}'"):
            raise InsertingStatsInDatabaseException()

    def get_current_month_requests(self):
        """
        Function to fecth current month requests
        """
        month = datetime.now().month
        year = datetime.now().year
        
        res = self._database.select(self._TABLE, "count(*)", f"month = {month} and year = {year}")

        if res:
            return res[0][0]
       
        raise FetchingStatsInDatabaseException()




        

    
    
