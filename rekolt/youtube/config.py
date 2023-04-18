from ..config import RekoltConfig

class RekoltYouTubeConfig:
    URLS = "urls"

    FORMAT = "format"
    FORMAT_PAR_DEFAUT = "mkv"
    __FORMAT_CODECS = {
        "mkv": "libx264"
    }

    QUALITE = "qualite"
    QUALITE_PAR_DEFAUT = 1080

    PROCESSUS_TELECHARGEMENT = "processus_telechargement"
    PROCESSUS_TELECHARGEMENT_PAR_DEFAUT = 2

    PROCESSUS_CONVERSION = "processus_conversion"
    PROCESSUS_CONVERSION_PAR_DEFAUT = 8

    SUPPRIMER_SOURCES = "supprimer_sources"
    SUPPRIMER_SOURCES_PAR_DEFAUT = True

    def __init__(self, config: RekoltConfig) -> None:
        self.__urls = set(config[RekoltYouTubeConfig.URLS])
        params = config.keys()
        # FORMAT
        if (RekoltYouTubeConfig.FORMAT in params):
            self.__format = int(config[RekoltYouTubeConfig.FORMAT])
        else:
            self.__format = RekoltYouTubeConfig.FORMAT_PAR_DEFAUT
        self.__codec = RekoltYouTubeConfig.__FORMAT_CODECS[self.__format]
        # QUALITE
        if (RekoltYouTubeConfig.QUALITE in params):
            self.__qualite = int(config[RekoltYouTubeConfig.QUALITE])
        else:
            self.__qualite = RekoltYouTubeConfig.QUALITE_PAR_DEFAUT
        # PROCESSUS TELECHARGEMENT
        if (RekoltYouTubeConfig.PROCESSUS_TELECHARGEMENT in params):
            self.__processus_telechargement = int(config[RekoltYouTubeConfig.PROCESSUS_TELECHARGEMENT])
        else:
            self.__processus_telechargement = RekoltYouTubeConfig.PROCESSUS_TELECHARGEMENT_PAR_DEFAUT
        # PROCESSUS CONVERSION
        if (RekoltYouTubeConfig.PROCESSUS_CONVERSION in params):
            self.__processus_conversion = int(config[RekoltYouTubeConfig.PROCESSUS_CONVERSION])
        else:
            self.__processus_conversion = RekoltYouTubeConfig.PROCESSUS_CONVERSION_PAR_DEFAUT
        # SUPPRESSION SOURCES
        if (RekoltYouTubeConfig.SUPPRIMER_SOURCES in params):
            self.__supprimer_sources = bool(config[RekoltYouTubeConfig.SUPPRIMER_SOURCES])
        else:
            self.__supprimer_sources = RekoltYouTubeConfig.SUPPRIMER_SOURCES_PAR_DEFAUT

    def urls(self) -> set[str] :
        return self.__urls
    
    def format(self) -> str :
        return self.__format
    
    def codec(self) -> str :
        return self.__codec
    
    def qualite(self) -> int :
        return self.__qualite
    
    def processus_telechargement(self) -> int :
        return self.__processus_telechargement
    
    def processus_conversion(self) -> int :
        return self.__processus_conversion
    
    def supprimer_sources(self) -> bool :
        return self.__supprimer_sources