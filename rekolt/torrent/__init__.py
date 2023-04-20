from ..terminal import RekoltTerminal
from ..modules import RekoltModule, RekoltConfig
from ..convert import RekoltConvert
from ..utils import NoPrint
from .config import RekoltTorrentConfig

from torrentp import TorrentInfo, TorrentDownloader
from threading import current_thread
from multiprocessing.dummy import Pool
import os, itertools

class RekoltTorrent(RekoltModule):
    NOM = "torrent"

    __TORRENT = ".torrent"
    __MAGNET = "magnet:"

    def __init__(self) -> None:
        super().__init__(RekoltTorrent.NOM, RekoltTorrentConfig)

    def __collecter(self, cible: str) -> list[str] :
        torrents = self.config().magnets()
        if (os.path.isdir(cible)):
            RekoltTerminal.afficher("Collecte des fichiers torrents depuis '" + cible + "'...")
            for torrent in [cible + os.path.sep + fichier for fichier in os.listdir(cible)]:
                if (torrent.endswith(RekoltTorrent.__TORRENT)):
                    torrents.append(torrent)
        return torrents

    def __telecharger(self, torrent: str, destination: str) -> None :
        torrent = str(torrent)
        magnet = torrent.startswith(RekoltTorrent.__MAGNET)
        nom = self.nouveau_thread("magnet" if magnet else "fichier")
        current_thread().setName(nom)
        destination = destination + os.path.sep
        if (magnet):
            RekoltTerminal.afficher("Téléchargement du torrent depuis le lien magnet vers '" + destination + "'...")
        else:
            destination += os.path.splitext(os.path.basename(torrent))[0]
            RekoltTerminal.afficher("Téléchargement du torrent '" + torrent + "' vers '" + destination + "'...")
        try:
            dl = TorrentDownloader(torrent, destination)
            if (self.config().progression()):
                dl.start_download()
            else:
                with NoPrint():
                    dl.start_download()
            RekoltTerminal.afficher("Téléchargement terminé.")
            if (self.config().conversion()):
                RekoltModule.modules()[RekoltConvert.NOM].convertir(destination)
        except Exception as e:
            RekoltTerminal.erreur(e)

    def invoquer(self, config: RekoltConfig) -> None :
        super().invoquer(config)
        if (self.config().conversion()):
            RekoltModule.modules()[RekoltConvert.NOM].debut_consommation()
        cible = config.destination() + os.path.sep + self.config().cible()
        torrents = self.__collecter(cible)
        iter_destination = itertools.repeat(config.destination() + os.path.sep + self.config().dossier())
        pool = Pool(self.config().processus())
        pool.starmap_async(self.__telecharger, zip(torrents, iter_destination))
        pool.close()
        pool.join()
        RekoltTerminal.afficher("Travail terminé.")
        if (self.config().conversion()):
            RekoltModule.modules()[RekoltConvert.NOM].fin_consommation()