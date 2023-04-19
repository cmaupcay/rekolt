from ..terminal import RekoltTerminal
from ..modules import RekoltModule, RekoltConfig
from .config import RekoltYouTubeConfig

from youtube_dl import YoutubeDL
from threading import current_thread
from multiprocessing.dummy import Pool
import os, itertools

class RekoltYouTube(RekoltModule):
    def __init__(self, modules: dict) -> None:
        super().__init__("youtube", RekoltYouTubeConfig, modules)

    def __options(self, destination: str) -> dict :
        return {
            "outtmpl": destination + os.path.sep + self.config().dossier() + os.path.sep + "%(title)s.%(ext)s",
            "format": "best[height<=" + str(self.config().qualite()) + "]",
            "nooverwrites": True,
            "ignoreerrors": True,
            "progress_hooks": [self.__hook],
            "logger": RekoltYouTube.__Logger()
        }

    def __collecter(self, url: str, options: dict) -> list[str] :
        RekoltTerminal.afficher("Collecte des éléments à télécharger depuis '" + url + "'...")
        dl = YoutubeDL(options)
        infos = dl.extract_info(url, download=False, process=False)
        return [video['url'] for video in infos['entries']]

    def __telecharger(self, url: str, options: dict) -> None :
        url = str(url)
        current_thread().setName(self.nouveau_nom_thread(url))
        RekoltTerminal.afficher("Téléchargement depuis '" + url + "'...")
        try:
            YoutubeDL(options).download([url])
        except Exception as e:
            RekoltTerminal.erreur(e)

    def __hook(self, infos: dict) -> None :
        if (infos['status'] == 'finished'):
            self.modules()['convert'].convertir(infos['filename'])

    def invoquer(self, config: RekoltConfig) -> None :
        super().invoquer(config)
        options = self.__options(config.destination())
        pool = Pool(self.config().processus())
        options_iter = itertools.repeat(options)
        for url in self.config().urls():
            videos = self.__collecter(url, options)
            pool.starmap_async(self.__telecharger, zip(videos, options_iter))
        pool.close()
        pool.join()
        self.modules()['convert'].ne_plus_attendre()

    class __Logger:
        def debug(self, msg: str) -> None :
            pass

        def warning(self, msg: str) -> None :
            RekoltTerminal.afficher(msg)

        def error(self, msg: str) -> None :
            RekoltTerminal.erreur(msg)