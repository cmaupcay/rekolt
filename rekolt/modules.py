from .config import Rekolt, RekoltConfig

from threading import current_thread, Thread

class RekoltModule(Thread):
    def __init__(self, nom: str, configClass: type, config: RekoltConfig, modules: dict) -> None:
        self.__nom = str(nom)
        self.__thread_prefix = Rekolt.NOM + '.' + nom + '.'
        self.__config = config.creer(configClass, self.__nom)
        self.__config_globale = config
        self.__modules = modules
        super().__init__(target=self.invoquer)

    def invoquer(self) -> None :
        current_thread().setName(Rekolt.NOM + '.' + self.__nom)

    def nom(self) -> str :
        return self.__nom
    
    def config(self):
        return self.__config
    
    def config_globale(self):
        return self.__config_globale
    
    def modules(self) -> dict :
        return self.__modules
    
    def nom_thread(self, nom: str) -> str :
        return self.__thread_prefix + nom

    def nouveau_thread(self, nom: str, cible: callable, *args) -> Thread :
        return Thread(name=self.nom_thread(nom), target=cible, args=args)