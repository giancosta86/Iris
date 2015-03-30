# -*- coding: utf-8 -*-

"""
:copyright: Copyright (C) 2013 Gianluca Costa.
:license: LGPLv3, see LICENSE for details.
"""


from __future__ import unicode_literals

import os

from ..vars import VariablesService, Flag
from ..io import PathOperations

from .tests_kernel import AbstractSiteTestCase


class VariablesTestCase(AbstractSiteTestCase):
	def setUp(self):
		super(VariablesTestCase, self).setUp()

		self._varsDir = os.path.join(self._siteDirPath, "_vars")
		self._variablesService = VariablesService(self._varsDir)


class VariablesServiceTests(VariablesTestCase):
	def testGetFlag(self):
		flag = self._variablesService.getFlag("myTestFlag")
		assert(flag is not None)		


class FlagTests(VariablesTestCase):
	def setUp(self):
		super(FlagTests, self).setUp()
		
		self._flagPath = os.path.join(self._varsDir, "SimpleTestFlag")
		
		PathOperations.safeRemove(self._flagPath)		
			
		self._flag = Flag(self._flagPath)
			
		
	def testGetPathAfterRetrievingTheInexistingFlag(self):
		self.assertEquals(
			self._flagPath, 
			self._flag.getPath()
		)
		
	
	def testIsActive(self):
		self.assertFalse(self._flag.isActive())
		
		
	def testActivate(self):
		self._flag.activate()
		self.assertTrue(self._flag.isActive())
		
	
	def testActivateCalledMultipleTimes(self):
		self._flag.activate()
		self._flag.activate()
		self.assertTrue(self._flag.isActive())
		
		
	def testDeactivate(self):
		self._flag.activate()
		self._flag.deactivate()
		self.assertFalse(self._flag.isActive())
		
	
	def testDeactivateCalledMultipleTimes(self):
		self._flag.activate()
		self._flag.deactivate()
		self._flag.deactivate()
		self.assertFalse(self._flag.isActive())
		
	
	def testFlipFromActiveToInactive(self):
		self._flag.activate()
		self._flag.flip()
		
		self.assertFalse(self._flag.isActive())
		
	
	def testFlipFromInactiveToActive(self):
		self._flag.deactivate()
		self._flag.flip()
		
		self.assertTrue(self._flag.isActive())