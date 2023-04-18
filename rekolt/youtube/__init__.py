from ..terminal import RekoltTerminal
from .config import RekoltConfig, RekoltYouTubeConfig

from youtube_dl import YoutubeDL
from multiprocessing.dummy import Pool as ThreadPool
import os, itertools

class RekoltYouTube:
    NOM = "RekoltYouTube"
    CONFIG = "youtube"

    def __init__(self) -> None:
        self.__config = None
        self.__fichiers = []

    class __Logger:
        def debug(self, msg: str) -> None :
            pass

        def warning(self, msg: str) -> None :
            RekoltTerminal.afficher(msg)

        def error(self, msg: str) -> None :
            RekoltTerminal.erreur(msg)

    def __options_telechargement(self, destination: str, config: RekoltYouTubeConfig) -> dict :
        return {
            "outtmpl": destination + os.path.sep + "%(title)s.%(ext)s",
            "format": "best[height<=" + str(config.qualite()) + "]",
            "postprocessors": [
                {
                    "key": "FFmpegVideoConvertor",
                    "preferedformat": config.format(),
                }
            ],
            "nooverwrites": True,
            "ignoreerrors": True,
            "progress_hooks": [self.__hook],
            "logger": RekoltYouTube.__Logger()
        }

    def __telecharger(self, url: str, options: dict) -> None :
        RekoltTerminal.afficher("Téléchargement depuis '" + str(url) + "'...")
        dl = YoutubeDL(options)
        dl.download([url])

    def __hook(self, infos: dict) -> None :
        status = infos['status']
        if (status == 'downloading'):
            fichier = infos['filename']
            if (fichier not in self.__fichiers):
                RekoltTerminal.afficher("Téléchargement de '" + fichier + "'...")
                self.__fichiers.append(fichier)
        elif (status == 'finished'):
            self.__convertir(infos['filename'])

    def invoquer(self, config: RekoltConfig) -> None :
        self.__config = config.creer(RekoltYouTubeConfig, RekoltYouTube.CONFIG)
        options = self.__options_telechargement(config.destination(), self.__config)
        pool = ThreadPool(self.__config.processus())
        pool.starmap(self.__telecharger, zip(self.__config.urls(), itertools.repeat(options)))
        pool.close()