from setuptools import setup
from setuptools import find_packages

setup(
        name = "hayai-cli",
        version = "1.0.0",
        description = "This is an application to download movies or shows from  streaming websites",
        author = "crypto",
        license = "MIT Licence",
        url = "https://github.com/crypto-0/hayai-cli",
        install_requires = ["click==8.0.4","lxml==4.9.2","pycryptodomex==3.17","httpx==0.23.3","tqdm==4.62.3","yarl==1.7.2","provider_parsers @ git+https://github.com/crypto-0/provider-parsers.git"],
        packages = find_packages(exclude=["tests","tests.downloader","tests.extractors","tests.extractors.utilities"]),
)
