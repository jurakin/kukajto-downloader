from setuptools import setup, find_packages

from src.kukajto_downloader import __version__

setup(
    name="kukajto-downloader",
    description="Finds the direct url of a video or subtitle file from kukaj.io",
    long_description=''.join(open("README.md", encoding="utf-8").readlines()),
    long_description_content_type="text/markdown",
    version=__version__,
    license="MIT",
    author_email="jurakin.dev@gmail.com",
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    url="https://github.com/jurakin/kukajto-downloader",
    keywords=["kukajto downloader", "kukaj", "kukajto", "downloader", "gui"],
    python_requires=">=3.7",
    install_requires=[
          "selenium>=4.7",
          "webdriver-manager",
          "eel",
          "requests",
          "tk",
    ],
    entry_points={
        "console_scripts": [
            "kukajto-downloader = kukajto_downloader.web.__main__:main",
        ]
    }
)