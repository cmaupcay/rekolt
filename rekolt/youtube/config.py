class RekoltYouTubeConfig:
    PLAYLISTS = "playlists"

    FORMAT = "format"
    FORMAT_PAR_DEFAUT = "mkv"

    QUALITE = "qualite"
    QUALITE_PAR_DEFAUT = 1080

    def __init__(self, config: dict) -> None:
        self.__playlists = set(config[RekoltYouTubeConfig.PLAYLISTS])
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

    def playlists(self) -> set[str] :
        return self.__playlists
    
    def format(self) -> str :
        return self.__format
    
    def qualite(self) -> int :
        return self.__qualite