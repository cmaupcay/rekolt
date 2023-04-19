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
        self.__destination = None

    def __convertir(self, source: str) -> None :
        destination = self.__destination + os.path.splitext(os.path.basename(source))[0]
        ext = '.' + self.config().format()
        tmp = destination + self.config().tmp() + ext
        destination += ext
        RekoltTerminal.afficher("Conversion de '" + str(source) + "' vers '" + destination + "'...")
        try:
            video = VideoFileClip(source)
            video.write_videofile(tmp, codec=self.config().codec(), threads=self.config().processus(), logger=None)
            os.rename(tmp, destination)
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

    def __ciblage(self, dossier: str) -> None :
        if (type(self.config().cible()) == str):
            cible = dossier + os.path.sep + self.config().cible() + os.path.sep
            if (os.path.isdir(cible)):
                RekoltTerminal.afficher("Chargement des éléments depuis '" + cible + "'...")
                for video in os.listdir(cible):
                    self.__fichiers.put(cible + video)

    def invoquer(self, config: RekoltConfig) -> None :
        super().invoquer(config)
        self.__ciblage(config.destination())
        RekoltTerminal.afficher("Démarrage...")
        self.__destination = config.destination() + os.path.sep + self.config().dossier() + os.path.sep
        self.__attendre = True
        while (self.__attendre or self.__fichiers.qsize() > 0):
            try:
                self.__convertir(self.__fichiers.get(timeout=RekoltConvert.__TIMEOUT))
            except Empty:
                pass