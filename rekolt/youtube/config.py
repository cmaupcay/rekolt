from ..config import RekoltConfig

class RekoltYouTubeConfig:
    URLS = "urls"

    QUALITE = "qualite"
    QUALITE_PAR_DEFAUT = 1080

    PROCESSUS = "processus"
    PROCESSUS_PAR_DEFAUT = 2

    def __init__(self, config: RekoltConfig) -> None:
        self.__urls = set(config[RekoltYouTubeConfig.URLS])
        params = config.keys()
        # QUALITE
        if (RekoltYouTubeConfig.QUALITE in params):
            self.__qualite = int(config[RekoltYouTubeConfig.QUALITE])
        else:
            self.__qualite = RekoltYouTubeConfig.QUALITE_PAR_DEFAUT
        # PROCESSUS
        if (RekoltYouTubeConfig.PROCESSUS in params):
            self.__processus = int(config[RekoltYouTubeConfig.PROCESSUS])
        else:
            self.__processus = RekoltYouTubeConfig.PROCESSUS_PAR_DEFAUT

    def urls(self) -> set[str] :
        return self.__urls
    
    def qualite(self) -> int :
        return self.__qualite
    
    def processus(self) -> int :
        return self.__processus