from ..terminal import RekoltTerminal
from ..modules import RekoltModule, RekoltConfig
from ..convert import RekoltConvert
from .config import RekoltYouTubeConfig

from youtube_dl import YoutubeDL
from threading import current_thread
from multiprocessing.dummy import Pool
import os, itertools

class RekoltYouTube(RekoltModule):
    NOM = "youtube"

    __TMPL = "%(title)s.%(ext)s"
    __VIDEO_URL = 'url'
    __INFOS_VIDEOS = 'entries'
    __INFOS_STATUS = 'status'
    __INFOS_STATUS_FINISHED = 'finished'
    __INFOS_FICHIER = 'filename'

    def __init__(self, config: RekoltConfig, modules: dict[str, RekoltModule]) -> None:
        super().__init__(RekoltYouTube.NOM, RekoltYouTubeConfig, config, modules)

    def __options(self, destination: str) -> dict :
        return {
            "outtmpl": destination + os.path.sep + self.config().dossier() + os.path.sep + RekoltYouTube.__TMPL,
            "format": "best[height<=" + str(self.config().qualite()) + "]",
            "nooverwrites": True,
            "ignoreerrors": True,
            "progress_hooks": [self.__hook],
            "logger": (None if self.config().progression() else RekoltYouTube.__Logger())
        }

    def __collecter(self, url: str, options: dict) -> list[str] :
        RekoltTerminal.afficher("Collecte des éléments à télécharger depuis '" + url + "'...")
        dl = YoutubeDL(options)
        infos = dl.extract_info(url, download=False, process=False)
        return [video[RekoltYouTube.__VIDEO_URL] for video in infos[RekoltYouTube.__INFOS_VIDEOS]]

    def __telecharger(self, url: str, options: dict) -> None :
        url = str(url)
        nom = self.nom_thread(url)
        current_thread().setName(nom)
        RekoltTerminal.afficher("Téléchargement depuis '" + url + "'...")
        try:
            dl = YoutubeDL(options)
            thread = self.nouveau_thread(url, dl.download, [url])
            thread.start()
            thread.join(self.config().delais())
            if (thread.is_alive()):
                raise TimeoutError("Délais dépassé : " + url)
        except Exception as e:
            RekoltTerminal.erreur(e)

    def __hook(self, infos: dict) -> None :
        if (infos[RekoltYouTube.__INFOS_STATUS] == RekoltYouTube.__INFOS_STATUS_FINISHED):
            RekoltTerminal.afficher("Téléchargement terminé.")
            if (self.config().conversion()):
                self.modules()[RekoltConvert.NOM].convertir(infos[RekoltYouTube.__INFOS_FICHIER])

    def invoquer(self) -> None :
        super().invoquer()
        if (self.config().conversion()):
            self.modules()[RekoltConvert.NOM].debut_consommation()
        options = self.__options(self.config_globale().destination())
        pool = Pool(self.config().processus())
        options_iter = itertools.repeat(options)
        for url in self.config().urls():
            videos = self.__collecter(url, options)
            pool.starmap_async(self.__telecharger, zip(videos, options_iter))
        pool.close()
        pool.join()
        RekoltTerminal.afficher("Travail terminé.")
        if (self.config().conversion()):
            self.modules()[RekoltConvert.NOM].fin_consommation()

    class __Logger:
        def debug(self, msg: str) -> None :
            pass

        def warning(self, msg: str) -> None :
            RekoltTerminal.afficher(msg)

        def error(self, msg: str) -> None :
            RekoltTerminal.erreur(msg)