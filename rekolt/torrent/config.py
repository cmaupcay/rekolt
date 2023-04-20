from ..config import RekoltConfigPrototype

class RekoltTorrentConfig(RekoltConfigPrototype):
    def __init__(self, config: dict[str, any]) -> None:
        super().__init__(config)

    CIBLE = "cible"
    def cible(self) -> str :
        return self._cible

    MAGNETS = "magnets"
    def magnets(self) -> list[str] :
        return self._magnets

    DOSSIER = "dossier"
    def dossier(self) -> str :
        return self._dossier

    PROCESSUS = "processus"
    def processus(self) -> int :
        return self._processus
    
    PROGRESSION = "progression"
    def progression(self) -> bool :
        return self._progression
    
    CONVERSION = "conversion"
    def conversion(self) -> bool :
        return self._conversion
    
    SUPPRIMER_SOURCES = "supprimer_sources"
    def supprimer_sources(self) -> bool :
        return self._supprimer_sources
    
    DELAIS = "delais"
    def delais(self) -> float :
        return self._delais

    __DESCRIPTION = {
        CIBLE: "torrent",
        MAGNETS: [],
        DOSSIER: "",
        PROCESSUS: 2,
        PROGRESSION: False,
        CONVERSION: False,
        SUPPRIMER_SOURCES: True,
        DELAIS: 14_400.0
    }    
    def description(self) -> dict[str, any]:
        return RekoltTorrentConfig.__DESCRIPTION