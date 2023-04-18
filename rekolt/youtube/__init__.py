from ..terminal import RekoltTerminal
from .config import RekoltConfig, RekoltYouTubeConfig

from youtube_dl import YoutubeDL
from moviepy.editor import VideoFileClip
from threading import Thread, current_thread
from multiprocessing.dummy import Pool
from queue import Queue, Empty
import os, itertools

class RekoltYouTube:
    NOM = "youtube"

    def __init__(self) -> None:
        self.__config = None
        self.__telechargements_termines = 0
        self.__conversions = Queue()
        self.__thread_prefix = ""

    def __options_telechargement(self, destination: str) -> dict :
        return {
            "outtmpl": destination + os.path.sep + "%(title)s.%(ext)s",
            "format": "best[height<=" + str(self.__config.qualite()) + "]",
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
        current_thread().setName(self.__thread_prefix + url)
        RekoltTerminal.afficher("Téléchargement depuis '" + url + "'...")
        YoutubeDL(options).download([url])

    def __hook(self, infos: dict) -> None :
        if (infos['status'] == 'finished'):
            self.__conversions.put(infos['filename'])

    def __convertir(self, source: str) -> None :
        destination = os.path.splitext(source)[0] + '.' + self.__config.format()
        RekoltTerminal.afficher("Conversion de '" + str(source) + "' vers '" + destination + "'...")
        video = VideoFileClip(source)
        video.write_videofile(destination, codec=self.__config.codec(), threads=self.__config.processus_conversion(), logger=None)
        video.close()
        if (self.__config.supprimer_sources() and os.path.isfile(destination)):
            RekoltTerminal.afficher("Suppression de la source '" + str(source) + "'...")
            os.remove(source)

    def __conversion(self) -> None :
        while (not self.__telechargements_termines or self.__conversions.qsize() > 0):
            try:
                self.__convertir(self.__conversions.get(timeout=1))
            except Empty:
                pass

    def invoquer(self, config: RekoltConfig) -> None :
        self.__config = config.creer(RekoltYouTubeConfig, RekoltYouTube.NOM)
        options = self.__options_telechargement(config.destination())
        self.__thread_prefix = current_thread().getName() + '-'
        conversion = Thread(name=self.__thread_prefix + "conversion", target=self.__conversion)
        self.__telechargements_termines = False
        conversion.start()
        telechargements = Pool(self.__config.processus_telechargement())
        options_iter = itertools.repeat(options)
        for url in self.__config.urls():
            videos = self.__collecter(url, options)
            telechargements.starmap_async(self.__telecharger, zip(videos, options_iter))
        telechargements.close()
        telechargements.join()
        self.__telechargements_termines = True
        conversion.join()

    class __Logger:
        def debug(self, msg: str) -> None :
            pass

        def warning(self, msg: str) -> None :
            RekoltTerminal.afficher(msg)

        def error(self, msg: str) -> None :
            RekoltTerminal.erreur(msg)