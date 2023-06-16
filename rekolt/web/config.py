from ..config import RekoltConfigPrototype

class RekoltWebConfig(RekoltConfigPrototype):
    def __init__(self, config: dict[str, any]) -> None:
        super().__init__(config)

    URLS = "urls"
    def urls(self) -> set[str] :
        return self._urls
    
    DOSSIER = "dossier"
    def dossier(self) -> str :
        return self._dossier

    QUALITE = "qualite"
    def qualite(self) -> int :
        return self._qualite
    
    PROCESSUS = "processus"
    def processus(self) -> int :
        return self._processus
    
    PROGRESSION = "progression"
    def progression(self) -> bool :
        return self._progression
    
    CONVERSION = "conversion"
    def conversion(self) -> bool :
        return self._conversion
    
    DELAIS = "delais"
    def delais(self) -> float :
        return self._delais
    
    FICHIERS = "fichiers"
    def fichiers(self) -> str :
        return self._fichiers

    __DESCRIPTION = {
        URLS: set,
        DOSSIER: "",
        QUALITE: 1080,
        PROCESSUS: 2,
        PROGRESSION: False,
        CONVERSION: True,
        DELAIS: 7200.0,
        FICHIERS: "%(title)s.%(ext)s"
    }

    def description(self) -> dict[str, any]:
        return RekoltWebConfig.__DESCRIPTION