from threading import current_thread
import sys

class RekoltTerminal:
    __SORTIE = sys.stdout

    def afficher(msg: str) -> None :
        print("[" + current_thread().getName() + "] " + msg, flush=True, file=RekoltTerminal.__SORTIE)

    def erreur(err: any) -> None :
        print("[" + current_thread().getName() + "] " + "/!\ " + str(err), flush=True, file=RekoltTerminal.__SORTIE)