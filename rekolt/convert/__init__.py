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
        self.__en_attente = Queue()
        self.__en_cours = None
        self.__destination = None

    def __convertir(self, source: str) -> None :
        self.__en_cours = source
        destination = os.path.splitext(os.path.basename(source))[0] + '.'
        tmp = self.__destination + self.config().tmp() + destination
        tmp_audio = tmp + "mp3"
        tmp += self.config().format()
        destination = self.__destination + destination + self.config().format()
        RekoltTerminal.afficher("Conversion de '" + str(source) + "' vers '" + destination + "'...")
        try:
            video = VideoFileClip(source)
            video.write_videofile(
                tmp,
                codec=self.config().codec(),
                threads=self.config().processus(),
                logger=("bar" if self.config().progression() else None),
                temp_audiofile=tmp_audio
            )
            os.rename(tmp, destination)
            video.close()
            if (self.config().supprimer_sources() and os.path.isfile(destination)):
                RekoltTerminal.afficher("Suppression de la source '" + str(source) + "'...")
                os.remove(source)
        except Exception as e:
            RekoltTerminal.erreur(e)
        self.__en_cours = None

    def attend(self) -> bool :
        return self.__attendre
    
    def ne_plus_attendre(self) -> None :
        self.__attendre = False

    def convertir(self, fichier: str) -> None :
        if (fichier == self.__en_cours or fichier in self.__en_attente.queue):
            RekoltTerminal.erreur("Le fichier '" + fichier + "' est déjà en cours ou en attente de traitement.")
        else:
            self.__en_attente.put(fichier)

    def __ciblage(self, dossier: str) -> None :
        if (type(self.config().cible()) == str):
            cible = dossier + os.path.sep + self.config().cible() + os.path.sep
            if (os.path.isdir(cible)):
                RekoltTerminal.afficher("Chargement des éléments depuis '" + cible + "'...")
                for video in os.listdir(cible):
                    if (os.path.splitext(video)[-1][1:] not in self.config().ignore()):
                        self.convertir(cible + video)

    def invoquer(self, config: RekoltConfig) -> None :
        super().invoquer(config)
        self.__ciblage(config.destination())
        RekoltTerminal.afficher("Démarrage...")
        self.__destination = config.destination() + os.path.sep + self.config().dossier() + os.path.sep
        self.__attendre = True
        while (self.__attendre or self.__en_attente.qsize() > 0):
            try:
                self.__convertir(self.__en_attente.get(timeout=RekoltConvert.__TIMEOUT))
            except Empty:
                pass