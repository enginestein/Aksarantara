from os import path
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))
import io

with io.open("README.md", "r", encoding="utf8") as f:
    long_description = f.read()

setup(
    name="Aksarantara",
    version="1.0.0",
    description="Transliteration framework for Indic language mainly focusing on Sanskrit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/enginestein/Aksarantara",
    author="Arya Praneil Pritesh",
    author_email="aryapraneil@gmail.com",
    license="GNU GPL 3.0",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    packages=find_packages(),
    install_requires=[
        "Requests>=2.20.1",
        "pykakasi>=2.0.6",
        "pyyaml>=5.4.1",
        "langcodes>=3.1.0",
        "language_data",
        "langcodes>=3.1.0",
        "language_data",
        "regex>=2021.8.3",
        "fonttools[unicode]>=4.27",
        "lxml",
    ],
    package_data={
        "aksarantara": [
            "data.yaml",
            "data.yaml",
            "data.json",
        ],
    },
)
