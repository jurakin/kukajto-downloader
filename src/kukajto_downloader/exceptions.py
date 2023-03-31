from .constants import KUKAJ_DOMAINS

class KukajError(Exception):
    message = "an error occured, please report an issue"
    def __init__(self, *args) -> None:
        if not args: args = [self.message]

        super().__init__(*args)


class UnsupportedStructureError(KukajError):
    message = "the structure of kukaj is not supported, please report an issue"


class UnsupportedSiteError(KukajError):
    message = f"the site domain must match one of ({', '.join(KUKAJ_DOMAINS)})"


class UnsupportedSourceError(KukajError):
    message = "the source is not currently supported, use other source please"