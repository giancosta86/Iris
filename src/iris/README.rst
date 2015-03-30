
Iris
~~~~~~

Iris is a general-purpose, object-oriented and open source 
Python library.

Iris is written in pure Python - it currently targets Python 2.7, 
but future support for Python 3 is planned.


Modules
--------

All the modules reside within the **iris** package.

The most interesting ones are perhaps:

* **iris.ioc**, featuring a simple IoC container, that supports transient and singleton objects out
  of the box and can be extended via OOP by introducing new registration kinds

* **iris.versioning**, introducing a *Version* class and a *VersionDirectory*, 
  that, for example, can return the file having the latest version in a directory

* **iris.maven**, dealing with *MavenArtifact* (which describes the Maven properties 
  of an artifact) and *MavenRepository*, to query a Maven repository using the concepts
  introduced in the **versioning** module

* **iris.web**, whose *Page* class renders a web page, including its headers, 
  ready to be returned as the output, for instance, of a CGI script. 
  *SiteInfoService* and *RequestInfoService* show,
  in a developer-friendly way, several important environment variables provided
  by an Apache web server.

* **iris.rendering** abstracts the templating process by providing a *Model* 
  class that can be easily reused with different rendering technologies 

* **iris.vars** enables developers to create boolean variables (instances of
  *Flag*) whose value depends on the existence of underlying files - 
  which can be useful in some situations where multiple technologies are involved

* **iris.io** introduces simple I/O utilities

* **iris.strings** provides a *String* utility class, foreseeing a future porting 
  to Python 3
  
  
What's new in version 1.2
-------------------------

* **iris.ioc**, a whole module dedicated to IoC and basic dependency injection

* some additions to **iris.io**, especially **PathOperations.linearWalk()** and
  **FileUtils.openEncoded()**