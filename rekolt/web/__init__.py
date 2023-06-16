from ..terminal import RekoltTerminal
from ..modules import RekoltModule, RekoltConfig
from ..convert import RekoltConvert
from .domaines import DOMAINES
from .config import RekoltWebConfig

from youtube_dl import YoutubeDL
from threading import current_thread
from multiprocessing.dummy import Pool

class RekoltWeb(RekoltModule):
    NOM = "web"

    __INFOS_STATUS = 'status'
    __INFOS_STATUS_FINISHED = 'finished'
    __INFOS_FICHIER = 'filename'

    def __init__(self, config: RekoltConfig, modules: dict[str, RekoltModule]) -> None:
        super().__init__(RekoltWeb.NOM, RekoltWebConfig, config, modules)

    def __telecharger(self, domaine: str, url: str, options: dict) -> None :
        url = str(url)
        current_thread().setName(self.nom_thread(domaine))
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
        if (infos[RekoltWeb.__INFOS_STATUS] == RekoltWeb.__INFOS_STATUS_FINISHED):
            RekoltTerminal.afficher("Téléchargement terminé.")
            if (self.config().conversion()):
                self.modules()[RekoltConvert.NOM].convertir(infos[RekoltWeb.__INFOS_FICHIER])

    def invoquer(self) -> None :
        super().invoquer()
        if (self.config().conversion()):
            self.modules()[RekoltConvert.NOM].debut_consommation()
        pool = Pool(self.config().processus())
        for url in self.config().urls():
            nonSupporte = True
            for domaine in DOMAINES:
                if (domaine.correspond(url)):
                    domaine.telecharger(url, self.config(), self.config_globale().destination(), pool, self.__telecharger, self.__hook)
                    nonSupporte = False
                    break
            if (nonSupporte):
                RekoltTerminal.erreur("Domaine non supporté : " + url)
        pool.close()
        pool.join()
        RekoltTerminal.afficher("Travail terminé.")
        if (self.config().conversion()):
            self.modules()[RekoltConvert.NOM].fin_consommation()