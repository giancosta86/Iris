# -*- coding: utf-8 -*-

"""
:copyright: Copyright (C) 2013 Gianluca Costa.
:license: LGPLv3, see LICENSE for details.
"""

#
# NOTE: for testing, string literals in this module 
# are "str" objects by default! Not Unicode!
#

import unittest

from ..strings import String


class StringsTests(unittest.TestCase):
	def testIsStringOnStrLiteral(self):
		self.assertTrue(String.isString("Test"))
		
		
	def testIsStringOnUnicodeLiteral(self):
		self.assertTrue(String.isString(u"Test"))
		
		
	def testStringOnStrInstance(self):
		testString = String("Test")
		
		self.assertIsInstance(testString, unicode)
		
		
	def testStringOnUnicodeInstance(self):
		testString = String(u"Test")
		
		self.assertIsInstance(testString, unicode)
		
	
	def testStringOnStrHavingAccents(self):
		testString = String("Voilà un example intéressant")
		
		self.assertIsInstance(testString, unicode)
		
	
	def testStringOnUnicodeHavingAccents(self):
		testString = String(u"Voilà un example intéressant")
		
		self.assertIsInstance(testString, unicode)
		
		
	def testStringOnIntInstance(self):
		testString = String(90)
				
		self.assertIsInstance(testString, unicode)
			