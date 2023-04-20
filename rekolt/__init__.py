from .app import Rekolt, RekoltApp, RekoltModule

from .convert import RekoltConvert
from .youtube import RekoltYouTube
from .torrent import RekoltTorrent

__MODULES = [
    RekoltYouTube,
    RekoltTorrent,
    RekoltConvert
]

def main() -> None :
    app = RekoltApp(__MODULES)
    app.start()
    app.join()
