from ..racine import Rekolt
from ..config import RekoltConfig

class RekoltConvertConfig:
    CIBLE = "cible"
    CIBLE_PAR_DEFAUT = None

    FORMAT = "format"
    FORMAT_PAR_DEFAUT = "mkv"
    __FORMAT_CODECS = {
        "mkv": "libx264"
    }

    DOSSIER = "dossier"
    DOSSIER_PAR_DEFAUT = ""

    TMP = "tmp"
    TMP_PAR_DEFAUT = '.' + Rekolt.NOM

    PROCESSUS = "processus"
    PROCESSUS_PAR_DEFAUT = 8

    SUPPRIMER_SOURCES = "supprimer_sources"
    SUPPRIMER_SOURCES_PAR_DEFAUT = True

    def __init__(self, config: RekoltConfig) -> None:
        params = config.keys()
        # CIBLE
        if (RekoltConvertConfig.CIBLE in params):
            self.__cible = str(config[RekoltConvertConfig.CIBLE])
        else:
            self.__cible = RekoltConvertConfig.CIBLE_PAR_DEFAUT
        # FORMAT
        if (RekoltConvertConfig.FORMAT in params):
            self.__format = int(config[RekoltConvertConfig.FORMAT])
        else:
            self.__format = RekoltConvertConfig.FORMAT_PAR_DEFAUT
        self.__codec = RekoltConvertConfig.__FORMAT_CODECS[self.__format]
        # DOSSIER
        if (RekoltConvertConfig.DOSSIER in params):
            self.__dossier = str(config[RekoltConvertConfig.DOSSIER])
        else:
            self.__dossier = RekoltConvertConfig.DOSSIER_PAR_DEFAUT
        # TMP
        if (RekoltConvertConfig.TMP in params):
            self.__tmp = str(config[RekoltConvertConfig.TMP])
        else:
            self.__tmp = RekoltConvertConfig.TMP_PAR_DEFAUT
        # PROCESSUS
        if (RekoltConvertConfig.PROCESSUS in params):
            self.__processus = int(config[RekoltConvertConfig.PROCESSUS])
        else:
            self.__processus = RekoltConvertConfig.PROCESSUS_PAR_DEFAUT
        # SUPPRESSION SOURCES
        if (RekoltConvertConfig.SUPPRIMER_SOURCES in params):
            self.__supprimer_sources = bool(config[RekoltConvertConfig.SUPPRIMER_SOURCES])
        else:
            self.__supprimer_sources = RekoltConvertConfig.SUPPRIMER_SOURCES_PAR_DEFAUT

    def cible(self) -> str | None :
        return self.__cible

    def format(self) -> str :
        return self.__format
    
    def codec(self) -> str :
        return self.__codec
    
    def dossier(self) -> str :
        return self.__dossier
    
    def tmp(self) -> str :
        return self.__tmp

    def processus(self) -> int :
        return self.__processus
    
    def supprimer_sources(self) -> bool :
        return self.__supprimer_sources