from .racine import Rekolt
from .config import RekoltConfig
from .terminal import RekoltTerminal
from .modules import RekoltModule

from threading import current_thread, Thread

class RekoltApp(Thread):
    def __init__(self, modules: list[type]) -> None :
        self.__modules = modules
        super().__init__(target=self.__main)

    def modules(self, config: RekoltConfig) -> dict[str, RekoltModule] :
        modules = {}
        for module in self.__modules:
            modules[module.NOM] = module(config, modules)
        return modules

    def __boucle(self, config: RekoltConfig) -> None :
        modules = self.modules(config)
        [modules[module].start() for module in modules]
        [modules[module].join() for module in modules]
    
    def __main(self) -> None :
        current_thread().setName(Rekolt.NOM)
        RekoltTerminal.afficher(Rekolt.NOM + " version " + Rekolt.VERSION)
        try:
            RekoltTerminal.afficher("Extraction de la configuration...")
            config = RekoltConfig.extraire()
            self.__boucle(config)
            while (config.boucle()):
                self.__boucle(config)
        except Exception as e:
            RekoltTerminal.erreur(e)