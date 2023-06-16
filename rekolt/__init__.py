from .app import Rekolt, RekoltApp, RekoltModule

from .convert import RekoltConvert
from .web import RekoltWeb
from .torrent import RekoltTorrent

__MODULES = [
    RekoltWeb,
    RekoltTorrent,
    RekoltConvert
]

def main() -> None :
    app = RekoltApp(__MODULES)
    app.start()
    app.join()
