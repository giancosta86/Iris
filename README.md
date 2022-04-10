# Iris

_General-purpose library for Python_

---

## Deprecation & namespace warning

**Please, note**: Iris is now deprecated and should be used only to support ancient projects.

Furthermore, for compatibility with Python's modern packaging system, please **delete from the file system every reference to its 3.x version** and use version 4.x instead.

---

## Introduction

Iris is a general-purpose, object-oriented and open source library for Python 3.

## Modules

All the modules reside within the **info.gianlucacosta.iris** package and subpackages.

In particular:

- **ioc**, featuring a simple IoC container, that supports transient and singleton objects out of the box and can be extended via OOP by introducing new registration kinds

- **versioning**, introducing a Version class and a VersionDirectory, that, for example, can return the file having the latest version in a directory

- **maven**, dealing with MavenArtifact (which describes the Maven properties of an artifact) and MavenRepository, to query a Maven repository using the concepts introduced in the versioning module

- **rendering** abstracts the templating process by providing a Model class that can be easily reused with different rendering technologies

- **vars** enables developers to create boolean variables (instances of Flag) whose value depends on the existence of underlying files - which can be useful in some situations where multiple technologies are involved

- **io.utils**, contains generic I/O utilities

- **io.tree** defines objects for operating on file trees

## Installation

Iris can be installed via **pip**:

> pip install info.gianlucacosta.iris
