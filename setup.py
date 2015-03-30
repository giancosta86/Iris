from setuptools import setup, find_packages
import glob

with open("README.rst", "r") as readmeFile:
    longDescription = readmeFile.read()

setup(
    name="Iris",
    version="2.0",
    packages=find_packages(),

    author="Gianluca Costa",
    author_email="gianluca@gianlucacosta.info",
    description="A general-purpose library for Python",
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

    test_suite="tests",

    scripts=glob.glob("scripts/*.py")
)