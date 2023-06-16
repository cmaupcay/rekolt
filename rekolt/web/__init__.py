from ..terminal import RekoltTerminal
from ..modules import RekoltModule, RekoltConfig
from ..convert import RekoltConvert
from .domaines import DOMAINES, RekoltWebDomaine
from .config import RekoltWebConfig

from youtube_dl import YoutubeDL
from threading import current_thread
from multiprocessing.dummy import Pool

class RekoltWeb(RekoltModule):
    NOM = "web"

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

    def __hook(self, domaine: RekoltWebDomaine) -> callable :
        def _hook(infos: dict) -> None :
            if (infos["status"] == "finished"):
                RekoltTerminal.afficher("Téléchargement terminé.")
                if (self.config().conversion()):
                    fichier = domaine.conversion(infos)
                    if (fichier != None):
                        self.modules()[RekoltConvert.NOM].convertir(fichier)
        return _hook

    def invoquer(self) -> None :
        super().invoquer()
        if (self.config().conversion()):
            self.modules()[RekoltConvert.NOM].debut_consommation()
        pool = Pool(self.config().processus())
        for url in self.config().urls():
            nonSupporte = True
            for domaine in DOMAINES:
                if (domaine.correspond(url)):
                    domaine.telecharger(url, self.config(), self.config_globale().destination(), pool, self.__telecharger, self.__hook(domaine))
                    nonSupporte = False
                    break
            if (nonSupporte):
                RekoltTerminal.erreur("Domaine non supporté : " + url)
        pool.close()
        pool.join()
        RekoltTerminal.afficher("Travail terminé.")
        if (self.config().conversion()):
            self.modules()[RekoltConvert.NOM].fin_consommation()