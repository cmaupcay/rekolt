from ..config import RekoltWebConfig
from ..logger import RekoltWebLogger, RekoltTerminal

from multiprocessing.dummy import Pool
from urllib.parse import urlparse
import os
import itertools

class RekoltWebDomaine:
    def __init__(self, nom: str, domaines: set[str]) :
        self.__nom = nom
        self.__domaines = domaines

    def nom(self) -> str:
        return self.__nom

    def correspond(self, url: str) -> bool :
        return urlparse(url).netloc in self.__domaines

    def conversion(self, infos: dict) -> str | None :
        return infos["filename"]

    __OPTION_HOOK = "progress_hooks"

    def options(self, config: RekoltWebConfig, destination: str) -> dict :
        return {
            "outtmpl": destination + os.path.sep + config.dossier() + os.path.sep + config.fichiers(),
            "nooverwrites": True,
            "ignoreerrors": True,
            RekoltWebDomaine.__OPTION_HOOK: [],
            "logger": (None if config.progression() else RekoltWebLogger())
        }
    
    def ressources(self, url: str, options: dict) -> list[str] :
        return [url]
    
    def telecharger(self, url: str, config: RekoltWebConfig, destination: str, threads: Pool, telecharger: callable, hook: callable) -> None :
        options = self.options(config, destination)
        options[RekoltWebDomaine.__OPTION_HOOK].append(hook)
        threads.starmap_async(telecharger, zip(itertools.repeat(self.__nom), self.ressources(url, options), itertools.repeat(options)))
