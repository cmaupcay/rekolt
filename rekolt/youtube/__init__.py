from ..terminal import RekoltTerminal
from .config import RekoltYouTubeConfig

from youtube_dl import YoutubeDL
import os

class RekoltYouTube:
    NOM = "RekoltYouTube"
    CONFIG = "youtube"

    # class Logger:
    #     def debug(self, msg: str) -> None :
    #         pass

    #     def warning(self, msg: str) -> None :
    #         RekoltTerminal.afficher(msg)

    #     def error(self, msg: str) -> None :
    #         RekoltTerminal.erreur(msg)

    # __LOGGER = Logger()

    # def __hook(infos: dict) -> None :
    #     if (infos['status'] == 'finished'):
    #         RekoltTerminal.afficher("Vidéo téléchargée (" + infos['filename'] + "). Conversion...")

    def __options(destination: str, config: RekoltYouTubeConfig) -> dict :
        return {
            "outtmpl": destination + os.path.sep + "%(title)s.%(ext)s",
            "format": "best[height<=" + str(config.qualite()) + "]",
            "postprocessors": [
                {
                    "key": "FFmpegVideoConvertor",
                    "preferedformat": config.format(),
                },
                {
                    "key": "ExecAfterDownload",
                    "exec_cmd": "rm {}"
                }
            ],
            "nooverwrites": True,
            "ignoreerrors": True,
            # "progress_hooks": [RekoltYouTube.__hook],
            # "logger": RekoltYouTube.__LOGGER
        }

    def invoquer(destination: str, config: dict) -> None :
        config = RekoltYouTubeConfig(config)
        dl = YoutubeDL(RekoltYouTube.__options(destination, config))
        RekoltTerminal.afficher("Téléchargement depuis " + str(len(config.playlists())) + " playlist(s)...")
        dl.download(config.playlists())