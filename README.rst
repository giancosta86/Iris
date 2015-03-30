
Iris
~~~~

Iris is a general-purpose, object-oriented and open source library for Python 3.


Modules
-------

All the modules reside within the **iris** package and subpackages.

The most interesting ones are perhaps:

* **iris.ioc**, featuring a simple IoC container, that supports transient and singleton objects out
  of the box and can be extended via OOP by introducing new registration kinds

* **iris.versioning**, introducing a *Version* class and a *VersionDirectory*, 
  that, for example, can return the file having the latest version in a directory

* **iris.maven**, dealing with *MavenArtifact* (which describes the Maven properties 
  of an artifact) and *MavenRepository*, to query a Maven repository using the concepts
  introduced in the **versioning** module

* **iris.rendering** abstracts the templating process by providing a *Model*
  class that can be easily reused with different rendering technologies 

* **iris.vars** enables developers to create boolean variables (instances of
  *Flag*) whose value depends on the existence of underlying files - 
  which can be useful in some situations where multiple technologies are involved

* **iris.io.utils**, formerly called **iris.io**, contains generic I/O utilities

* **iris.io.tree** defines objects for operating on file trees



What's new in version 2
-----------------------

* Full Python 3 support. Python 2 is no more supported

* a few *utility scripts* are provided

* **iris.strings** has been removed, in favor of Python 3's string handling

* **iris.web** has been removed. WebPath can be replaced by Python's Path class

