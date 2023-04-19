from ..config import RekoltConfig

class RekoltConvertConfig:
    FORMAT = "format"
    FORMAT_PAR_DEFAUT = "mkv"
    __FORMAT_CODECS = {
        "mkv": "libx264"
    }

    PROCESSUS = "processus"
    PROCESSUS_PAR_DEFAUT = 8

    SUPPRIMER_SOURCES = "supprimer_sources"
    SUPPRIMER_SOURCES_PAR_DEFAUT = True

    def __init__(self, config: RekoltConfig) -> None:
        params = config.keys()
        # FORMAT
        if (RekoltConvertConfig.FORMAT in params):
            self.__format = int(config[RekoltConvertConfig.FORMAT])
        else:
            self.__format = RekoltConvertConfig.FORMAT_PAR_DEFAUT
        self.__codec = RekoltConvertConfig.__FORMAT_CODECS[self.__format]
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

    def format(self) -> str :
        return self.__format
    
    def codec(self) -> str :
        return self.__codec
    
    def processus(self) -> int :
        return self.__processus
    
    def supprimer_sources(self) -> bool :
        return self.__supprimer_sources