from .racine import Rekolt
from .config import RekoltConfig
from .terminal import RekoltTerminal

from .youtube import RekoltYouTube

__MODULES = [
    RekoltYouTube
]

def main() -> None :
    try:
        RekoltTerminal.afficher("Extraction de la configuration...")
        config = RekoltConfig.extraire()
        configs = config.keys()
        for module in __MODULES:
            RekoltTerminal.afficher("Module : " + module.NOM)
            RekoltTerminal.indenter()
            if (module.CONFIG in configs):
                module.invoquer(Rekolt.DESTINATION, config[module.CONFIG])
            else:
                RekoltTerminal.erreur("Pas de configuration détectée.")
            RekoltTerminal.desindenter()
    except Exception as e:
        RekoltTerminal.retablir()
        RekoltTerminal.erreur(e)
