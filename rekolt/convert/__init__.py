from ..terminal import RekoltTerminal
from ..modules import RekoltModule, RekoltConfig
from .config import RekoltConvertConfig

from moviepy.editor import VideoFileClip
from queue import Queue, Empty
import os

class RekoltConvert(RekoltModule):
    NOM = "convert"

    __AUDIO_EXT = "mp3"
    __TIMEOUT = 1

    def __init__(self, config: RekoltConfig, modules: dict[str, RekoltModule]) -> None:
        super().__init__(RekoltConvert.NOM, RekoltConvertConfig, config, modules)
        self.__consommateurs = 0
        self.__en_attente = Queue()
        self.__en_cours = None
        self.__destination = None

    def __convertir(self, source: str) -> None :
        self.__en_cours = source
        destination = os.path.splitext(os.path.basename(source))[0] + '.'
        tmp = self.__destination + self.config().tmp() + destination
        tmp_audio = tmp + RekoltConvert.__AUDIO_EXT
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

    def debut_consommation(self) -> None :
        self.__consommateurs += 1

    def fin_consommation(self) -> None :
        self.__consommateurs -= 1

    def convertir(self, cible: str) -> None :
        if (cible == self.__en_cours or cible in self.__en_attente.queue):
            RekoltTerminal.erreur("Le fichier '" + cible + "' est déjà en cours ou en attente de traitement.")
        else:
            if (os.path.isdir(cible)):
                for fichier in os.listdir(cible):
                    self.convertir(cible + os.path.sep + fichier)
            elif (os.path.isfile(cible)):
                if (os.path.splitext(cible)[-1][1:] not in self.config().ignore()):
                    self.__en_attente.put(cible)
            else:
                RekoltTerminal.erreur("Le fichier '" + cible + "' n'existe pas.")

    def __ciblage(self, dossier: str) -> None :
        if (len(self.config().cible()) > 0):
            cible = dossier + os.path.sep + self.config().cible() + os.path.sep
            if (os.path.isdir(cible)):
                RekoltTerminal.afficher("Chargement des éléments depuis '" + cible + "'...")
                for video in os.listdir(cible):
                    self.convertir(cible + video)

    def invoquer(self) -> None :
        super().invoquer()
        self.__ciblage(self.config_globale().destination())
        self.__destination = self.config_globale().destination() + os.path.sep + self.config().dossier() + os.path.sep
        while (self.__consommateurs > 0 or self.__en_attente.qsize() > 0):
            try:
                self.__convertir(self.__en_attente.get(timeout=RekoltConvert.__TIMEOUT))
            except Empty:
                pass
        RekoltTerminal.afficher("Travail terminé.")