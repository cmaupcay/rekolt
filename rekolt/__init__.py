from .racine import Rekolt
from .config import RekoltConfig
from .terminal import RekoltTerminal
from .modules import RekoltModule

from .convert import RekoltConvert
from .youtube import RekoltYouTube
from .torrent import RekoltTorrent

from threading import current_thread, Thread

def __init() -> None :
    RekoltModule.ajouter_module(RekoltYouTube())
    RekoltModule.ajouter_module(RekoltTorrent())
    RekoltModule.ajouter_module(RekoltConvert())

def main() -> None :
    current_thread().setName(Rekolt.NOM)
    RekoltTerminal.afficher(Rekolt.NOM + " version " + Rekolt.VERSION)
    __init()
    try:
        RekoltTerminal.afficher("Extraction de la configuration...")
        config = RekoltConfig.extraire()
        modules = RekoltModule.modules().values()
        modules_threads = []
        for module in modules:
            thread = Thread(name=Rekolt.NOM + '.' + module.nom(), target=module.invoquer, args=(config,))
            thread.start()
            modules_threads.append(thread)
        for module in modules_threads:
            module.join()
    except Exception as e:
        RekoltTerminal.retablir()
        RekoltTerminal.erreur(e)
