from ..terminal import RekoltTerminal
from ..modules import RekoltModule, RekoltConfig
from .config import RekoltConvertConfig

from moviepy.editor import VideoFileClip
from queue import Queue, Empty
import os

class RekoltConvert(RekoltModule):
    __TIMEOUT = 1

    def __init__(self, modules: dict) -> None:
        super().__init__("convert", RekoltConvertConfig, modules)
        self.__attendre = False
        self.__fichiers = Queue()

    def __convertir(self, source: str) -> None :
        destination = os.path.splitext(source)[0] + '.' + self.config().format()
        RekoltTerminal.afficher("Conversion de '" + str(source) + "' vers '" + destination + "'...")
        try:
            video = VideoFileClip(source)
            video.write_videofile(destination, codec=self.config().codec(), threads=self.config().processus(), logger=None)
            video.close()
            if (self.config().supprimer_sources() and os.path.isfile(destination)):
                RekoltTerminal.afficher("Suppression de la source '" + str(source) + "'...")
                os.remove(source)
        except Exception as e:
            RekoltTerminal.erreur(e)

    def attend(self) -> bool :
        return self.__attendre
    
    def ne_plus_attendre(self) -> None :
        self.__attendre = False

    def convertir(self, fichier: str) -> None :
        self.__fichiers.put(fichier)

    def invoquer(self, config: RekoltConfig) -> None :
        super().invoquer(config)
        if (type(self.config().cible()) == str):
            destination = config.destination() + os.path.sep + self.config().cible()
            if (os.path.isdir(destination)):
                RekoltTerminal.afficher("Chargement des éléments depuis '" + destination + "'...")
                for video in os.listdir(destination):
                    self.__fichiers.put(video)
        RekoltTerminal.afficher("Démarrage...")
        self.__attendre = True
        while (self.__attendre or self.__fichiers.qsize() > 0):
            try:
                self.__convertir(self.__fichiers.get(timeout=RekoltConvert.__TIMEOUT))
            except Empty:
                pass