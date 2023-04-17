from .racine import Rekolt

import json

class RekoltConfig:
    def extraire(fichier = Rekolt.FICHIER) -> dict :
        flux = open(fichier, 'r', encoding=Rekolt.ENCODAGE)
        config = flux.readlines()
        flux.close()
        return json.loads(str.join('\n', config))