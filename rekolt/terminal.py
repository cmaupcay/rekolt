from .racine import Rekolt

class RekoltTerminal:
    __PREFIX = "[" + Rekolt.NOM + "] "

    __INDENTATION = 0

    def afficher(msg: str) -> None :
        print(RekoltTerminal.__PREFIX + (RekoltTerminal.__INDENTATION * '\t') + msg, flush=True)

    def erreur(err: any) -> None :
        print(RekoltTerminal.__PREFIX + (RekoltTerminal.__INDENTATION * '\t') + "/!\ " + str(err), flush=True)

    def indenter() -> None :
        RekoltTerminal.__INDENTATION += 1

    def desindenter() -> None :
        RekoltTerminal.__INDENTATION -= 1

    def retablir() -> None :
        RekoltTerminal.__INDENTATION = 0