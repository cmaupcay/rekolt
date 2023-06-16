from .domaine import RekoltWebDomaine, RekoltTerminal

from playwright.sync_api import sync_playwright, Response

class RekoltWebArte(RekoltWebDomaine):
    def __init__(self) :
        super().__init__("arte", ("www.arte.tv"))
        self.__ressources = []

    def __extraire(self, reponse: Response) -> None :
        if (reponse.url.endswith(".m3u8") and ("VF-STF" in reponse.url)):
            self.__ressources.append(reponse.url)

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