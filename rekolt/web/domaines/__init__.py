from .domaine import RekoltWebDomaine
from .youtube import RekoltWebYouTube
from .arte import RekoltWebArte

DOMAINES: list[RekoltWebDomaine] = [
    RekoltWebYouTube(),
    RekoltWebArte()
]