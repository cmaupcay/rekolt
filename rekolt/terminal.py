from threading import current_thread

class RekoltTerminal:
    def afficher(msg: str) -> None :
        print("[" + current_thread().getName() + "] " + msg, flush=True)

    def erreur(err: any) -> None :
        print("[" + current_thread().getName() + "] " + "/!\ " + str(err), flush=True)