# -*- coding: utf-8 -*-

"""
:copyright: Copyright (C) 2013 Gianluca Costa.
:license: LGPLv3, see LICENSE for details.
"""

from __future__ import unicode_literals

import unittest
import os

from ..web import WebPath, SiteInfoService, RequestInfoService, Page
from ..strings import String


class WebPathTests(unittest.TestCase):
	def testIsAbsoluteOnAbsolutePath(self):
		webPath = WebPath("/test/tau/")
		assert(webPath.isAbsolute())

	def testIsAbsoluteOnRelativePath(self):
		webPath = WebPath("test/tau2/")
		assert(not webPath.isAbsolute())

	def testCastingToStringOnAbsolutePath(self):
		webPathString = "/test/tau/"
		webPath = WebPath(webPathString)
		self.assertEquals(webPathString, String(webPath))


	def testCastingToStringOnRelativePath(self):
		webPathString = "test/tau/"
		webPath = WebPath(webPathString)
		self.assertEquals(webPathString, String(webPath))


	def testGetAbsoluteOnAbsolutePath(self):
		webPath = WebPath("/test/tau")
		assert(webPath.getAbsolute(None).isAbsolute())


	def testEqualityOfStringAndAbsolutePath(self):
		webPathString = "/test/tau/"
		webPath = WebPath(webPathString)
		self.assertEquals(webPathString, webPath)

	def testEqualityOfStringAndRelativePath(self):
		webPathString = "test/tau/"
		webPath = WebPath(webPathString)
		self.assertEquals(webPathString, webPath)


	def testEqualityOfAbsoluteWebPaths(self):
		webPathString = "/test/tau/"
		referenceWebPath = WebPath(webPathString)
		webPath = WebPath(webPathString)
		self.assertEquals(referenceWebPath, webPath)


	def testEqualityOfRelativeWebPaths(self):
		webPathString = "test/tau/"
		referenceWebPath = WebPath(webPathString)
		webPath = WebPath(webPathString)
		self.assertEquals(referenceWebPath, webPath)


	def testGetAbsoluteWhenTheReferenceStringHasATrailingSlash(self):
		webPath = WebPath("alpha")
		absWebPath = webPath.getAbsolute("/test/tau/")
		self.assertEquals("/test/tau/alpha", absWebPath)


	def testGetAbsoluteWhenTheReferenceStringHasNoTrailingSlash(self):
		webPath = WebPath("alpha")
		absWebPath = webPath.getAbsolute("/test/tau")
		self.assertEquals("/test/tau/alpha", absWebPath)
		

	def testGetAbsoluteWhenTheReferenceWebPathHasATrailingSlash(self):
		webPath = WebPath("alpha")
		absWebPath = webPath.getAbsolute(WebPath("/test/tau/"))
		self.assertEquals("/test/tau/alpha", absWebPath)


	def testGetAbsoluteWhenTheReferenceWebPathHasNoTrailingSlash(self):
		webPath = WebPath("alpha")
		absWebPath = webPath.getAbsolute(WebPath("/test/tau"))
		self.assertEquals("/test/tau/alpha", absWebPath)

	def testAddOnAbsoluteLeftOperand(self):
		leftWebPath = WebPath("/alpha")
		rightWebPath = "beta"
		self.assertEquals("/alpha/beta", leftWebPath + rightWebPath)

	def testAddOnRelativeLeftOperand(self):
		leftWebPath = WebPath("alpha")
		rightWebPath = "beta"
		self.assertEquals("alpha/beta", leftWebPath + rightWebPath)


	def testGetParentOnThreeLevelsOfAbsolutePath(self):
		webPath = WebPath("/alpha/beta/gamma")
		self.assertEquals("/alpha/beta", webPath.getParent())


	def testGetParentWithThreeLevelsOfRelativePath(self):
		webPath = WebPath("alpha/beta/gamma")
		self.assertEquals("alpha/beta", webPath.getParent())


	def testGetParentOnOneLevelOfAbsolutePath(self):
		webPath = WebPath("/alpha")
		self.assertEquals("/", webPath.getParent())

	def testGetParentOnOneLevelOfRelativePath(self):
		webPath = WebPath("alpha")
		self.assertIs(None, webPath.getParent())
		
		
	def testGetFileNameOnRootAbsoluteLevel(self):
		webPath = WebPath("/myfile.bmp")
		self.assertEquals("myfile.bmp", webPath.getFileName())
		
		
	def testGetFileNameOnhOneAbsoluteLevel(self):
		webPath = WebPath("/dir1/myfile.bmp")
		self.assertEquals("myfile.bmp", webPath.getFileName())
		
		
	def testGetFileNameOnTwoAbsoluteLevels(self):
		webPath = WebPath("/dir1/dir2/myfile.bmp")
		self.assertEquals("myfile.bmp", webPath.getFileName())
		
		
		
	def testGetFileNameOnRootRelativeLevel(self):
		webPath = WebPath("myfile.bmp")
		self.assertEquals("myfile.bmp", webPath.getFileName())
		
		
	def testGetFileNameOnOneRelativeLevel(self):
		webPath = WebPath("dir1/myfile.bmp")
		self.assertEquals("myfile.bmp", webPath.getFileName())
		
		
	def testGetFileNameOnTwoRelativeLevels(self):
		webPath = WebPath("dir1/dir2/myfile.bmp")
		self.assertEquals("myfile.bmp", webPath.getFileName())
	
	
	
class SiteInfoServiceTests(unittest.TestCase):

	def setUp(self):
		self._fakeDocumentRoot = os.path.join("fake", "usr", "dir")
		os.environ["DOCUMENT_ROOT"] = self._fakeDocumentRoot
		self._siteInfoService = SiteInfoService()

	def testGetRootPath(self):
		self.assertEquals(self._fakeDocumentRoot, self._siteInfoService.getRootPath())

	def testGetPathOnAbsolutePathString(self):
		path = self._siteInfoService.getPath("/website/test.htm")
		self.assertEquals(os.path.join("fake", "usr", "dir", "website", "test.htm"), path)

	def testGetPathOnRelativePathString(self):
		self.assertRaises(AssertionError, self._siteInfoService.getPath, "website/test.htm")



class RequestInfoServiceTests(unittest.TestCase):
	def setUp(self):
		self._requestWebPath = WebPath("/web/service/test")
		self._requestScriptWebPath = WebPath("/web/service/test.py")

		os.environ["REQUEST_URI"] = String(self._requestWebPath)
		os.environ["SCRIPT_NAME"] = String(self._requestScriptWebPath)
		self._requestInfoService = RequestInfoService()


	def testGetRequestScriptWebPath(self):
		self.assertEquals(self._requestScriptWebPath, self._requestInfoService.getRequestScriptWebPath())


	def testGetRequestWebPath(self):
		self.assertEquals(self._requestWebPath, self._requestInfoService.getRequestWebPath())


	def testGetAbsolutePathWhenThePassedPathIsAbsolute(self):
		path = "/software/test/x.htm"

		self.assertEquals(path, self._requestInfoService.getAbsoluteWebPath(path))

	def testGetAbsolutePathWhenThePassedPathIsRelative(self):
		path = "software/test/x.htm"
		absolutePath = self._requestInfoService.getAbsoluteWebPath(path)
		self.assertEquals("/web/service/software/test/x.htm", String(absolutePath))


	def testIsInDebuggingWhenServerEndsWithLocalHost(self):
		os.environ["SERVER_NAME"] = "mytest.alpha.localhost"
		self.assertTrue(self._requestInfoService.isInDebugging())	


	def testIsInDebuggingWhenServerDoesNotEndWithLocalHost(self):
		os.environ["SERVER_NAME"] = "mytest.beta"
		self.assertFalse(self._requestInfoService.isInDebugging())
		
		
	def testGetServerName(self):
		serverName = "test.localhost"
		os.environ["SERVER_NAME"] = serverName
		
		self.assertEquals(serverName, self._requestInfoService.getServerName())
		
		
	def testGetServerPort(self):
		serverPort = "80"
		os.environ["SERVER_PORT"] = serverPort
		
		self.assertEquals(serverPort, self._requestInfoService.getServerPort())
		
		
	def testGetCookieString(self):
		os.environ["HTTP_COOKIE"] = "My cookie string"
		self.assertEquals("My cookie string", self._requestInfoService.getCookieString())
		
		


class PageTests(unittest.TestCase):
	def testPageRenderingOnAnIntegerView(self):				
		pageContent = 90
		
		pageMimeType = "text/plain"
		pageEncoding = "utf-8"
		
		page = Page(pageContent, pageMimeType, pageEncoding)
		
		expectedRendering = "Content-Type: {0}; charset={1}\r\n\r\n{2}".format(pageMimeType, pageEncoding, pageContent)
		
		self.assertEquals(expectedRendering, String(page))
		
		
	def testAddHeader(self):				
		pageContent = 90
		
		pageMimeType = "text/plain"
		pageEncoding = "utf-8"
		
		page = Page(pageContent, pageMimeType, pageEncoding)
		
		page.addHeader("Max-Forwards: 15")
		
		expectedRendering = "Content-Type: {0}; charset={1}\r\nMax-Forwards: 15\r\n\r\n{2}".format(pageMimeType, pageEncoding, pageContent)
		
		self.assertEquals(expectedRendering, String(page))

		
		
	def testPageRenderingOnAStringHavingAccents(self):				
		pageContent = """
		Hello, this is a test page.
		It contains multiple lines of text.
		C'è anche, però, qualche carattere accentato.
		Et voilà, bien évidemment, d'autres accents.		
		"""
		
		pageMimeType = "text/plain"
		pageEncoding = "utf-8"
		
		page = Page(pageContent, pageMimeType, pageEncoding)
		
		expectedRendering = "Content-Type: {0}; charset={1}\r\n\r\n{2}".format(pageMimeType, pageEncoding, pageContent)
		
		self.assertEquals(expectedRendering, String(page))