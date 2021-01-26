import os

from setuptools import find_packages, setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="opentunes-api",
    version="0.0.1",
    description="An API for your music",
    long_description=read("README.rst"),
    license="GPL",
    author="Ingo Weinmann",
    author_email="mail@ingoweinmann.de",
    url="https://github.com/wolkenarchitekt/opentunes-api",
    packages=find_packages(),
    zip_safe=True,
    include_package_data=True,
    install_requires=["fastapi",],
)
