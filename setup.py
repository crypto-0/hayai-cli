from setuptools import setup
from setuptools import find_packages

setup(
        name = "providers",
        version = "1.0.0",
        description = "This is a library to interact with streaming websites",
        author = "crypto",
        license = "MIT Licence",
        url = "https://github.com/crypto-0/provider-parsers",
        install_requires = ["click==8.0.4","lxml==4.9.2","pycryptodomex==3.17"],
        packages = find_packages(exclude=["tests","tests.extractors","tests.extractors.utilities"]),
)
