import setuptools
from setuptools import version

with open('requirements.txt', 'r') as reqs:
    requirements = reqs.read().splitlines()

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="downchecker",
    version="0.0.1",
    author="",
    description="",
    long_description=long_description,
    packages=['downchecker'],
    install_requires=[requirements],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 1 - Planning",
    ],
    python_requires='>=3.6',
)
