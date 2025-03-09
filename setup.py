from setuptools import setup, find_packages
from pathlib import Path
CURRENT_DIR = Path(__file__).resolve().parent
requeriments = []
with open(CURRENT_DIR.joinpath("requirements.txt"), "r") as file:
    requeriments = file.read().splitlines()

setup(
    name="endstone plugin builder",  
    version="1.7",
    packages=find_packages(),
    install_requires=requeriments,
    entry_points={
        "console_scripts": [
            "build=source.main:main"
        ]
    },
    author="ensinolats",
    description="easy way of building your endstone plugins in a valid file",
)