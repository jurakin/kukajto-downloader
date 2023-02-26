class BaseError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class UnsupportedStructureError(BaseError):
    pass


class UnsupportedSiteError(BaseError):
    pass


class UnsupportedSourceError(BaseError):
    pass


class DownloadError(BaseError):
    pass
