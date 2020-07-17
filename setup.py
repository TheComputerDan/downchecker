import setuptools
from setuptools import version

with open("README.md","r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="downchecker",
    version="0.0.1",
    author="",
    description="",
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)