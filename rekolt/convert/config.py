from ..config import RekoltConfigPrototype

class RekoltConvertConfig(RekoltConfigPrototype):
    __FORMAT_CODECS = {
        "mkv": "libx264"
    }

    def __init__(self, config: dict[str, any]) -> None:
        super().__init__(config)
        if (self._ignore_format):
            self._ignore.add(self._format)
        self.__codec = RekoltConvertConfig.__FORMAT_CODECS[self._format]

    CIBLE = "cible"
    def cible(self) -> str | None :
        return self._cible
    
    IGNORE = "ignore"
    def ignore(self) -> set[str] :
        return self._ignore
    
    IGNORE_FORMAT = "ignore_format"
    def ignore_format(self) -> bool :
        return self._ignore_format

    FORMAT = "format"
    def format(self) -> str :
        return self._format
    
    def codec(self) -> str :
        return self.__codec
    
    DOSSIER = "dossier"
    def dossier(self) -> str :
        return self._dossier
    
    TMP = "tmp"
    def tmp(self) -> str :
        return self._tmp

    PROCESSUS = "processus"
    def processus(self) -> int :
        return self._processus
    
    PROGRESSION = "progression"
    def progression(self) -> bool :
        return self._progression
    
    SUPPRIMER_SOURCES = "supprimer_sources"
    def supprimer_sources(self) -> bool :
        return self._supprimer_sources
    
    ATTENTE = "attente"
    def attente(self) -> float :
        return self._attente
    
    __DESCRIPTION = {
        CIBLE: "",
        IGNORE: {"part", "txt", "nfo", "torrent"},
        FORMAT: "mkv",
        IGNORE_FORMAT: True,
        DOSSIER: "",
        TMP: ".",
        PROCESSUS: 8,
        PROGRESSION: False,
        SUPPRIMER_SOURCES: True,
        ATTENTE: 5.0
    }

    def description(self) -> dict[str, any] :
        return RekoltConvertConfig.__DESCRIPTION