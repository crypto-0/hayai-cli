from setuptools import setup
from setuptools import find_packages

setup(
        name = "hayai-cli",
        version = "1.0.0",
        description = "This is an application to stream/play movies or shows from  streaming websites",
        author = "crypto",
        license = "MIT Licence",
        url = "https://github.com/crypto-0/hayai-cli",
        install_requires = ["click==8.0.4","lxml==4.9.2","pycryptodomex==3.17","m3u8=3.4.0","tqdm==4.62.3","tqdm==4.62.3","requests==2.28.2","setuptools==67.6.1"],
        packages = find_packages(exclude=["tests","tests.downloader","tests.extractors","tests.extractors.utilities"]),
)
