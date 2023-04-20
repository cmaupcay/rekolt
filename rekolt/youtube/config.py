from ..config import RekoltConfig

class RekoltYouTubeConfig:
    URLS = "urls"

    DOSSIER = "dossier"
    DOSSIER_PAR_DEFAUT = ""

    QUALITE = "qualite"
    QUALITE_PAR_DEFAUT = 1080

    PROCESSUS = "processus"
    PROCESSUS_PAR_DEFAUT = 2

    PROGRESSION = "progression"
    PROGRESSION_PAR_DEFAUT = False

    CONVERSION = "conversion"
    CONVERSION_PAR_DEFAUT = True

    TIMEOUT = "timeout"
    TIMEOUT_PAR_DEFAUT = 1200;

    def __init__(self, config: RekoltConfig) -> None:
        self.__urls = set(config[RekoltYouTubeConfig.URLS])
        params = config.keys()
        # DOSSIER
        if (RekoltYouTubeConfig.DOSSIER in params):
            self.__dossier = str(config[RekoltYouTubeConfig.DOSSIER])
        else:
            self.__dossier = RekoltYouTubeConfig.DOSSIER_PAR_DEFAUT
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
        # PROGRESSION
        if (RekoltYouTubeConfig.PROGRESSION in params):
            self.__progression = bool(config[RekoltYouTubeConfig.PROGRESSION])
        else:
            self.__progression = RekoltYouTubeConfig.PROGRESSION_PAR_DEFAUT
        # CONVERSION
        if (RekoltYouTubeConfig.CONVERSION in params):
            self.__conversion = bool(config[RekoltYouTubeConfig.CONVERSION])
        else:
            self.__conversion = RekoltYouTubeConfig.CONVERSION_PAR_DEFAUT
        # TIMEOUT
        if (RekoltYouTubeConfig.TIMEOUT in params):
            self.__timeout = int(config[RekoltYouTubeConfig.TIMEOUT])
        else:
            self.__timeout = RekoltYouTubeConfig.TIMEOUT_PAR_DEFAUT

    def urls(self) -> set[str] :
        return self.__urls
    
    def dossier(self) -> str :
        return self.__dossier

    def qualite(self) -> int :
        return self.__qualite
    
    def processus(self) -> int :
        return self.__processus
    
    def progression(self) -> bool :
        return self.__progression
    
    def conversion(self) -> bool :
        return self.__conversion
    
    def timeout(self) -> int :
        return self.__timeout