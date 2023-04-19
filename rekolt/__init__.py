from .racine import Rekolt
from .config import RekoltConfig
from .terminal import RekoltTerminal

from .convert import RekoltConvert
from .youtube import RekoltYouTube

from threading import current_thread, Thread

__MODULES = []

def __init() -> None :
    __MODULES.append(RekoltConvert(__MODULES))
    __MODULES.append(RekoltYouTube(__MODULES))

def main() -> None :
    current_thread().setName(Rekolt.NOM)
    RekoltTerminal.afficher(Rekolt.NOM + " version " + Rekolt.VERSION)
    __init()
    try:
        RekoltTerminal.afficher("Extraction de la configuration...")
        config = RekoltConfig.extraire()
        modules_threads = []
        for module in __MODULES:
            thread = Thread(name=Rekolt.NOM + '.' + module.nom(), target=module.invoquer, args=(config,))
            thread.start()
            modules_threads.append(thread)
        for module in modules_threads:
            module.join()
    except Exception as e:
        RekoltTerminal.retablir()
        RekoltTerminal.erreur(e)
