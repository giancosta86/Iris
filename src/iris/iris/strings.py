# -*- coding: utf-8 -*-

"""
String-related utilities, mainly used for
future compatibility with Python 3

:copyright: Copyright (C) 2013 Gianluca Costa.
:license: LGPLv3, see LICENSE for details.
"""
from __future__ import unicode_literals


class String(object):
	"""
	Returns the unicode representation of the 
	given value, using the given encoding (defaults to "utf-8")
	"""
	
	def __new__(cls, value, encoding="utf-8"):	
		if isinstance(value, unicode):
			return value
		
		if isinstance(value, str):
			return unicode(value, encoding)
		
		
		return unicode(value)
		
	
	
	@staticmethod
	def isString(obj):
		"""
		Returns true if the given object is a string 
		(both str and unicode are considered strings)
		"""
		return isinstance(obj, basestring)