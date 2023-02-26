from kukajto_downloader.wrapper import Kukaj

from kukajto_downloader.exceptions import BaseError
from kukajto_downloader.exceptions import UnsupportedSiteError
from kukajto_downloader.exceptions import UnsupportedSourceError
from kukajto_downloader.exceptions import UnsupportedStructureError

__all__ = [
    "Kukaj",
    
    "BaseError",
    "UnsupportedSiteError",
    "UnsupportedSourceError",
    "UnsupportedStructureError",
]

__version__ = "1.1"