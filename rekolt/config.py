from .racine import Rekolt

import json

class RekoltConfig:
    DESTINATION = "destination"

    def __init__(self, config: dict) -> None:
        if (RekoltConfig.DESTINATION in config.keys()):
            self.__destination = str(config[RekoltConfig.DESTINATION])
            config.pop(RekoltConfig.DESTINATION)
        else:
            self.__destination = Rekolt.DESTINATION
        self.__config = config.copy()

    def destination(self) -> str :
        return self.__destination
    
    def modules(self) -> set[str] :
        return set(self.__config.keys())
    
    def creer(self, config, champs: str | None = None):
        return config(self.__config if champs == None else self.__config[champs])

    def extraire(fichier = Rekolt.FICHIER):
        flux = open(fichier, 'r', encoding=Rekolt.ENCODAGE)
        config = flux.readlines()
        flux.close()
        return RekoltConfig(json.loads(str.join('\n', config)))