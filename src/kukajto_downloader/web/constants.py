from os.path import dirname

ASSETS_DIR = dirname(__file__) + "/assets"
HOME_PAGE = "https://kukaj.io/"

VIDEO_SUFFIX = ".mp4"
SUBS_SUFFIX = ".vtt"

CHUNK_SIZE = 1 << 20 # 1 MiB

DRIVER_MANAGER_DIR = r"." # default driver installation directory