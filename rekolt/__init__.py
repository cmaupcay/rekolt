from .racine import Rekolt
from .config import RekoltConfig
from .terminal import RekoltTerminal

from .youtube import RekoltYouTube

from threading import current_thread, Thread

__MODULES = [
    RekoltYouTube()
]

def main() -> None :
    current_thread().setName(Rekolt.NOM)
    RekoltTerminal.afficher(Rekolt.NOM + " version " + Rekolt.VERSION)
    try:
        RekoltTerminal.afficher("Extraction de la configuration...")
        config = RekoltConfig.extraire()
        modules = config.modules()
        modules_threads = []
        for module in __MODULES:
            if (module.NOM in modules):
                thread = Thread(name=Rekolt.NOM + '-' + module.NOM, target=module.invoquer, args=(config,))
                thread.start()
                modules_threads.append(thread)
            else:
                RekoltTerminal.erreur("Pas de configuration détectée pour le module.")
        for module in modules_threads:
            module.join()
    except Exception as e:
        RekoltTerminal.retablir()
        RekoltTerminal.erreur(e)
