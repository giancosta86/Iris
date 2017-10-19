import glob

from setuptools import setup, find_packages


with open("README.md", "r") as readmeFile:
    longDescription = readmeFile.read()

setup(
    name="info.gianlucacosta.iris",
    version="3.1",
    packages=find_packages(),

    author="Gianluca Costa",
    author_email="gianluca@gianlucacosta.info",
    description="General-purpose library for Python",
    long_description=longDescription,
    license="LGPLv3",
    keywords=["library", "IoC container", "dependency injector", "versioning", "Maven", "rendering", "utilities"],
    url="https://github.com/giancosta86/Iris",

    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Utilities"
    ],

    test_suite="info.gianlucacosta.iris.tests",

    scripts=glob.glob("scripts/*.py")
)
