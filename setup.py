from setuptools import setup, find_packages
from src.paralell_downloader import __version__

setup(
    name="paralell-downloader",
    description="Downloads file using paralell downloading.",
    version=__version__,
    license="GNU General Public License v3.0",
    author_email="jurakin.dev@gmail.com",
    packages=find_packages("src"),
    package_dir={"": "src"},
    url="https://github.com/jurakin/paralell-downloader",
    keywords="paralell downloader",
    python_requires='>=3.7',
    install_requires=[
          "requests",
      ],
)