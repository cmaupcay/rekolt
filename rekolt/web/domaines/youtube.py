from ..config import RekoltWebConfig
from .domaine import RekoltWebDomaine, RekoltTerminal

from youtube_dl import YoutubeDL

class RekoltWebYouTube(RekoltWebDomaine):
    def __init__(self) :
        super().__init__("youtube", ("www.youtube.com", "youtu.be"))

    __VIDEO_URL = 'url'
    __INFOS_VIDEOS = 'entries'

    def options(self, config: RekoltWebConfig, destination: str) -> dict :
        opts = super().options(config, destination)
        opts["format"] = "best[height<=" + str(config.qualite()) + "]"
        return opts
    
    def ressources(self, url: str, options: dict) -> list[str] :
        RekoltTerminal.afficher("Collecte des vidéos à télécharger depuis '" + url + "'...")
        dl = YoutubeDL(options)
        infos = dl.extract_info(url, download=False, process=False)
        return [video[RekoltWebYouTube.__VIDEO_URL] for video in infos[RekoltWebYouTube.__INFOS_VIDEOS]]