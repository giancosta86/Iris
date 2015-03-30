# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.rst", "r") as readmeFile:
	longDescription = readmeFile.read()

setup(
    name = "Iris",
    version = "1.3",
    packages = find_packages(),
    
    author = "Gianluca Costa",
    author_email = "gianluca@gianlucacosta.info",
    description = "A general-purpose library for Python",
    long_description = longDescription,
    license = "LGPLv3",
    keywords = ["library", "IoC container", "dependency injector", "versioning", "Maven", "web", "web path", "server info", "HTTP request", "rendering", "utilities"],
    url = "http://gianlucacosta.info/software/iris/",
    
    classifiers = [
		"Development Status :: 5 - Production/Stable",
		"Intended Audience :: Developers",
		"License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
		"Operating System :: OS Independent",
		"Programming Language :: Python",
		"Topic :: Internet :: WWW/HTTP",		
		"Topic :: Utilities"
	],
    
    test_suite = "iris.tests"
)