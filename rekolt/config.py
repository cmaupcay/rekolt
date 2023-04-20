from .racine import Rekolt

import json

class RekoltConfigPrototype:
    def __init__(self, config: dict[str, any]) -> None:
        description = self.description()
        defs = config.keys()
        for param in description:
            param_t = type(description[param])
            val = None
            if (param in defs):
                if (param_t == type):
                    param_t = description[param]
                val = param_t(config[param])
                config.pop(param)
            elif (param_t == type):
                raise ValueError(param)
            else:
                val = description[param]
            self.__setattr__("_" + param, val)

    def description(self) -> dict[str, any] :
        return {}

class RekoltConfig(RekoltConfigPrototype):
    DESTINATION = "destination"

    BOUCLE = "boucle"

    __DESCRIPTION = {
        DESTINATION: Rekolt.DESTINATION,
        BOUCLE: False
    }

    def __init__(self, config: dict[str, any]) -> None:
        super().__init__(config)
        self.__config = config.copy()

    def description(self) -> dict[str, any]:
        return RekoltConfig.__DESCRIPTION

    def destination(self) -> str :
        return self._destination
    
    def boucle(self) -> bool :
        return self._boucle

    def modules(self) -> set[str] :
        return set(self.__config.keys())
    
    def creer(self, config: type, champs: str | None = None):
        return config(self.__config if champs == None else (self.__config[champs] if champs in self.__config.keys() else {}))

    def extraire(fichier = Rekolt.FICHIER):
        flux = open(fichier, 'r', encoding=Rekolt.ENCODAGE)
        config = flux.readlines()
        flux.close()
        return RekoltConfig(json.loads(str.join('\n', config)))