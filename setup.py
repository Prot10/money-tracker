"""Setuptools installation file for the package."""

from pathlib import Path

from setuptools import find_packages, setup

required = Path("requirements.txt").read_text().splitlines()

setup(
    name="app",
    version="0.1.0",
    packages=find_packages(),
    python_requires=">=3.11",
    install_requires=required,
)
