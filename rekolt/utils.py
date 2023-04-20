import os, sys

class NoPrint:
    def __enter__(self) -> None:
        self.__stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        sys.stdout.close()
        sys.stdout = self.__stdout