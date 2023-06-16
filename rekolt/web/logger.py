from ..terminal import RekoltTerminal

class RekoltWebLogger:
    def debug(self, msg: str) -> None :
        pass

    def warning(self, msg: str) -> None :
        RekoltTerminal.afficher(msg)

    def error(self, msg: str) -> None :
        RekoltTerminal.erreur(msg)