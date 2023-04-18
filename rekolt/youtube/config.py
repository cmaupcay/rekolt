from ..config import RekoltConfig

class RekoltYouTubeConfig:
    URLS = "urls"

    FORMAT = "format"
    FORMAT_PAR_DEFAUT = "mkv"

    QUALITE = "qualite"
    QUALITE_PAR_DEFAUT = 1080

    PROCESSUS = "processus"
    PROCESSUS_PAR_DEFAUT = 4

    def __init__(self, config: RekoltConfig) -> None:
        self.__urls = set(config[RekoltYouTubeConfig.URLS])
        # FORMAT
        if (RekoltYouTubeConfig.FORMAT in config.keys()):
            self.__format = int(config[RekoltYouTubeConfig.FORMAT])
        else:
            self.__format = RekoltYouTubeConfig.FORMAT_PAR_DEFAUT
        # QUALITE
        if (RekoltYouTubeConfig.QUALITE in config.keys()):
            self.__qualite = int(config[RekoltYouTubeConfig.QUALITE])
        else:
            self.__qualite = RekoltYouTubeConfig.QUALITE_PAR_DEFAUT
        # PROCESSUS
        if (RekoltYouTubeConfig.PROCESSUS in config.keys()):
            self.__processus = int(config[RekoltYouTubeConfig.PROCESSUS])
        else:
            self.__processus = RekoltYouTubeConfig.PROCESSUS_PAR_DEFAUT

    def urls(self) -> set[str] :
        return self.__urls
    
    def format(self) -> str :
        return self.__format
    
    def qualite(self) -> int :
        return self.__qualite
    
    def processus(self) -> int :
        return self.__processus