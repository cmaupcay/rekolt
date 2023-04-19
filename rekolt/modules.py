from .config import RekoltConfig

from threading import current_thread

class RekoltModule:
    def __init__(self, nom: str, configClass: type, modules: list) -> None:
        self.__nom = nom
        self.__configClass = configClass
        self.__modules = {}
        for module in modules:
            self.__modules[module.nom()] = module
        self.__config = None
        self.__thread_prefix = None

    def invoquer(self, config: RekoltConfig) -> None :
        self.__config = config.creer(self.__configClass, self.__nom)
        self.__thread_prefix = current_thread().getName() + '.'

    def nom(self) -> str :
        return self.__nom
    
    def config(self):
        return self.__config
    
    def modules(self) -> dict :
        return self.__modules
    
    def nouveau_nom_thread(self, nom: str) -> str :
        return self.__thread_prefix + nom