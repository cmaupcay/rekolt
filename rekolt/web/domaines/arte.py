from ..config import RekoltWebConfig
from .domaine import RekoltWebDomaine, RekoltTerminal

from playwright.sync_api import sync_playwright, Response
import time
import os

class RekoltWebArte(RekoltWebDomaine):
    __IDS = ["VF-STF_XQ", "VOF_XQ", "VOF-STF_XQ"]

    def __init__(self) :
        super().__init__("arte", ("www.arte.tv"))
        self.__ressources = []
        self.__termines = []

    def options(self, config: RekoltWebConfig, destination: str) -> dict :
        opts = super().options(config, destination)
        opts["format"] = "(bestvideo+bestaudio/best)"
        return opts

    def __extraire(self, reponse: Response) -> None :
        for id in RekoltWebArte.__IDS:
            if (reponse.url.endswith(id + ".m3u8")):
                self.__ressources.append(reponse.url)
                break

    def ressources(self, url: str, options: dict) -> list[str] :
        RekoltTerminal.afficher("Extraction des éléments à télécharger depuis '" + url + "'...")
        self.__ressources = []
        with sync_playwright() as p:
            nav = p.firefox.launch()
            page = nav.new_page()
            page.on("response", self.__extraire)
            page.goto(url, wait_until="networkidle")
            page.context.close()
            nav.close()
        return self.__ressources

    def conversion(self, infos: dict) -> str | None :
        fichier = infos["filename"].split('.')[0] + ".mp4"
        if (fichier in self.__termines):
            return fichier
        else:
            self.__termines.append(fichier)
            return None