# -*- coding: utf-8 -*-

"""
Web tools 

:copyright: Copyright (C) 2013 Gianluca Costa.
:license: LGPLv3, see LICENSE for details.
"""

from __future__ import unicode_literals

import os
import re

from iris.strings import String


class WebPath(object):
	"""
	A path in the context of a web server.
	
	A path can be:
	
	-- absolute, if starting with "/"
	-- relative, otherwise
	"""
	
	_parentPattern = re.compile(r"^(.*)/[^/]*$")
	_fileNamePattern = re.compile(r"^(?:.*/)*([^/]+)$")

	def __init__(self, source):
		"""
		Creates the web path, using the string representation of its source
		"""
		assert(source is not None)

		self._sourceString = String(source)


	def __str__(self):
		return self._sourceString


	def __cmp__(self, other):
		"""
		Two web paths are compared on their source string
		"""
		return cmp(self._sourceString, String(other))


	def isAbsolute(self):
		"""
		Returns true if the web path is absolute
		"""
		return self._sourceString.startswith("/")


	def getAbsolute(self, referenceWebPath):
		"""
		Joins the reference web path (which must be absolute) 
		and this web path to obtain an absolute web path.
		
		However, if this web path is already absolute, the reference
		web path is not considered.
		"""
		if (self.isAbsolute()):
			return self

		referenceWebPath = WebPath(referenceWebPath)

		assert(referenceWebPath.isAbsolute())

		return referenceWebPath + self		


	def __add__(self, relativeWebPath):
		"""
		You can sum any web path with a relative web path.
		
		The / characters in the joining point are not duplicated.
		"""
		relativeWebPath = WebPath(relativeWebPath)

		assert(not relativeWebPath.isAbsolute())

		return WebPath("{0}/{1}".format(
			self._sourceString.rstrip("/"),
			relativeWebPath
		))


	def getParent(self):
		"""
		Returns the parent of the given web path.
		
		Note:
		
		--for an absolute web path, another absolute web path
		  is always returned (even just "/" if called on a
		  first-level absolute web path such as "/alpha" or "/beta"
		  
		--for a relative web path, another relative web path is
		  returned *or None*, if the relative web path has just one
		  component (such as just "alpha" or "beta")
		"""
		match = self._parentPattern.match(self._sourceString)

		if match is None:
			return None

		parentSource = match.group(1)
		if parentSource == "":
			return WebPath("/")

		return WebPath(parentSource)
	
	
	def getFileName(self):
		"""
		Returns the file name of the path, ie, the part after the last "/"
		"""
		match = self._fileNamePattern.match(self._sourceString)
		
		return match.group(1)
		


class SiteInfoService(object):
	"""
	Provides information about global server and Iris variables,
	as well as related methods.
	"""
	def getRootPath(self):		
		return os.environ["DOCUMENT_ROOT"]


	def getPath(self, absoluteWebPath):
		"""
		Returns the on-disk path of the given absolute web path
		"""
		assert(absoluteWebPath is not None)
		absoluteWebPathString = String(absoluteWebPath)
		assert(absoluteWebPathString.startswith("/"))

		webPathComponent = absoluteWebPathString.lstrip("/").replace("/", os.sep)
		return os.path.join(self.getRootPath(), webPathComponent)



class RequestInfoService(object):
	"""
	Provides information about request variables,
	as well as the related methods
	"""
	
	def getServerName(self):
		"""
		The server name associated with this request
		"""
		return os.environ["SERVER_NAME"]


	def isLocal(self):
		"""
		Returns true if the server name ends with "localhost"
		"""
		return self.getServerName().endswith("localhost")


	def isInDebugging(self):
		"""
		By default, a synonym of isLocal()
		"""
		return self.isLocal()


	def getServerPort(self):
		"""
		Returns the server port for the current request
		"""
		return os.environ["SERVER_PORT"]


	def getRequestWebPath(self):
		"""
		Returns the WebPath of the current request
		"""
		return WebPath(os.environ["REQUEST_URI"])


	def getRequestScriptWebPath(self):
		"""
		Returns the WebPath of the script serving the current request
		"""
		return WebPath(os.environ["SCRIPT_NAME"])


	def getCookieString(self):
		"""
		Returns the cookie string for this request
		"""
		return os.environ.get("HTTP_COOKIE")


	def getAbsoluteWebPath(self, webPath):
		"""
		If the passed web path is absolute, returns it unchanged;
		otherwise, it concatenates it to the parent of the current 
		request web path.
		"""
		webPath = WebPath(webPath)

		if webPath.isAbsolute():
			return webPath
		else:
			return webPath.getAbsolute(self.getRequestScriptWebPath().getParent())


class Page(object):
	"""
	A page served by a web server - not necessarily HTML-based.
	"""
	
	def __init__(self, view, contentType="text/html", charset="utf-8"):
		"""
		The web page requires a view - which is simply an object 
		that can be meaningfully converted to a string.
		
		--"contentType" is used to generate the related header
		--"charset" is used both for the Content-Type header and 
		  to convert the view to a unicode string 
		"""
		
		self._headers = [
			 "Content-Type: {0}; charset={1}".format(contentType, charset)
		 ]
		self._charset = charset
		
		self._view = view


	def addHeader(self, header):
		"""
		Adds a header to the page
		"""
		self._headers.append(header)

	
	def __str__(self):
		"""
		Converts the page to an HTTP-compliant string, that can be
		returned by a web server (for example, as a CGI output)
		"""
		resultComponents = [String(header) + "\r\n" for header in self._headers]
		
		resultComponents.append("\r\n")
		
		resultComponents.append(String(self._view))
		
		result = "".join(resultComponents)
		
		return String(result).encode(self._charset)	