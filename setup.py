#!/usr/bin/env python3
from distutils.core import setup

setup(
    name="pauseonlock",
    version="0.1",
    description="Pause/Resume your media players on screen locking/unlocking",
    author="Thomas Goldbrunner",
    author_email="thomas.goldbrunner@posteo.de",
    py_modules=["pauseonlock"],
    entry_points={"console_scripts": ["pauseonlock=pauseonlock:main"]},
    install_requires=["dbus-next>=0.2.2"],
    extras_require={
        "dev": [
            "pytest",
            "black",
            "flake8",
            "flake8-bugbear",
            "pycodestyle",
        ]
    },
)
