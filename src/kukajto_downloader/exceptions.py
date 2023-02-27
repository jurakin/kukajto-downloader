class KukajError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class UnsupportedStructureError(KukajError):
    pass


class UnsupportedSiteError(KukajError):
    pass


class UnsupportedSourceError(KukajError):
    pass


class DownloadError(KukajError):
    pass
