from .config import RekoltConfig

from threading import current_thread

class RekoltModule:
    __MODULES = {}

    def __init__(self, nom: str, configClass: type) -> None:
        self.__nom = nom
        self.__configClass = configClass
        self.__config = None
        self.__thread_prefix = None

    def invoquer(self, config: RekoltConfig) -> None :
        self.__config = config.creer(self.__configClass, self.__nom)
        self.__thread_prefix = current_thread().getName() + '.'

    def nom(self) -> str :
        return self.__nom
    
    def config(self):
        return self.__config
    
    def modules() -> dict :
        return RekoltModule.__MODULES

    def ajouter_module(module) -> None :
        RekoltModule.__MODULES[module.nom()] = module
    
    def nouveau_thread(self, nom: str) -> str :
        return self.__thread_prefix + nom