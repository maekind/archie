# encoding:utf-8

"""
rae.py - drae inteface to make online searches
"""

from pyrae import dle
import logging

class RaeInterface():
    """
    Class to provide methods to search words in online RAE dictionary
    """

    def __init__(self):
        """
        Default constructor
        """
        self._logger = logging.getLogger("RAE interface")

    def __repr__(self) -> str:
        """ Return a printed version """
        return f"{self.__class__.__name__}"

    def search(self, word):
        """
        Method to search a word in the RAE dictionary
        """
        self._logger.info(f"Searching for word {word}")
        definitions = []
        result = dle.search_by_word(word=word)
        
        try:
            # Get main object
            articles = result.to_dict().get("articles")[0]
            
            # Iter definitions
            for definition in articles.get("definitions"):
                index = definition.get("index")
                category = definition.get("category").get("text")
                sentence = definition.get("sentence").get("text")
                
                # Create dict
                definition_dict = {}
                definition_dict.update({"index": index})
                definition_dict.update({"category": category})
                definition_dict.update({"definition": sentence})
                
                # Save defintion into list
                definitions.append(definition_dict)

        except Exception as e:
            self._logger.error(f"{word} not found!")
            return None

        return definitions


if __name__ == "__main__":
    logargs = {
        'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        'datefmt': '%Y-%m-%d %H:%M:%S'}

    logargs["level"] = "INFO"

    logging.basicConfig(**logargs)

    rae = RaeInterface()
    definitions = rae.search("rozar")
    logging.info(definitions)

