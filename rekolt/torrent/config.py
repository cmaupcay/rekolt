from ..config import RekoltConfig

class RekoltTorrentConfig:
    CIBLE = "cible"
    CIBLE_PAR_DEFAUT = "torrent"

    MAGNETS = "magnets"
    MAGNETS_PAR_DEFAUT = []

    DOSSIER = "dossier"
    DOSSIER_PAR_DEFAUT = ""

    PROCESSUS = "processus"
    PROCESSUS_PAR_DEFAUT = 2

    PROGRESSION = "progression"
    PROGRESSION_PAR_DEFAUT = False

    CONVERSION = "conversion"
    CONVERSION_PAR_DEFAUT = False

    SUPPRIMER_SOURCES = "supprimer_sources"
    SUPPRIMER_SOURCES_PAR_DEFAUT = True

    TIMEOUT = "timeout"
    TIMEOUT_PAR_DEFAUT = 7200.0;

    def __init__(self, config: RekoltConfig) -> None:
        params = config.keys()
        # CIBLE
        if (RekoltTorrentConfig.CIBLE in params):
            self.__cible = str(config[RekoltTorrentConfig.CIBLE])
        else:
            self.__cible = RekoltTorrentConfig.CIBLE_PAR_DEFAUT
        # MAGNETS
        if (RekoltTorrentConfig.MAGNETS in params):
            self.__magnets = config[RekoltTorrentConfig.MAGNETS]
        else:
            self.__magnets = RekoltTorrentConfig.MAGNETS_PAR_DEFAUT
        # DOSSIER
        if (RekoltTorrentConfig.DOSSIER in params):
            self.__dossier = str(config[RekoltTorrentConfig.DOSSIER])
        else:
            self.__dossier = RekoltTorrentConfig.DOSSIER_PAR_DEFAUT
        # PROCESSUS
        if (RekoltTorrentConfig.PROCESSUS in params):
            self.__processus = int(config[RekoltTorrentConfig.PROCESSUS])
        else:
            self.__processus = RekoltTorrentConfig.PROCESSUS_PAR_DEFAUT
        # PROGRESSION
        if (RekoltTorrentConfig.PROGRESSION in params):
            self.__progression = bool(config[RekoltTorrentConfig.PROGRESSION])
        else:
            self.__progression = RekoltTorrentConfig.PROGRESSION_PAR_DEFAUT
        # CONVERSION
        if (RekoltTorrentConfig.CONVERSION in params):
            self.__conversion = bool(config[RekoltTorrentConfig.CONVERSION])
        else:
            self.__conversion = RekoltTorrentConfig.CONVERSION_PAR_DEFAUT
        # SUPPRESSION SOURCES
        if (RekoltTorrentConfig.SUPPRIMER_SOURCES in params):
            self.__supprimer_sources = bool(config[RekoltTorrentConfig.SUPPRIMER_SOURCES])
        else:
            self.__supprimer_sources = RekoltTorrentConfig.SUPPRIMER_SOURCES_PAR_DEFAUT
        # TIMEOUT
        if (RekoltTorrentConfig.TIMEOUT in params):
            self.__timeout = float(config[RekoltTorrentConfig.TIMEOUT])
        else:
            self.__timeout = RekoltTorrentConfig.TIMEOUT_PAR_DEFAUT

    def cible(self) -> str :
        return self.__cible

    def magnets(self) -> list[str] :
        return self.__magnets

    def dossier(self) -> str :
        return self.__dossier

    def processus(self) -> int :
        return self.__processus
    
    def progression(self) -> bool :
        return self.__progression
    
    def conversion(self) -> bool :
        return self.__conversion
    
    def supprimer_sources(self) -> bool :
        return self.__supprimer_sources
    
    def timeout(self) -> int :
        return self.__timeout