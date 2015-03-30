# -*- coding: utf-8 -*-

"""
:copyright: Copyright (C) 2013 Gianluca Costa.
:license: LGPLv3, see LICENSE for details.
"""

from __future__ import unicode_literals

import unittest

from ..rendering import Model, View, TemplateView


class TestModel(Model):
	def getAlpha(self):
		return 90
	
	def getBeta(self):
		return "Test!"
	
	def isTesting(self):
		return True
	
	

class ModelTests(unittest.TestCase):
	def setUp(self):
		self._model = TestModel(False)
		
		self._expectedVars = {
			"alpha": self._model.getAlpha(),
			"beta": self._model.getBeta(),
			"testing": self._model.isTesting()			
		}		
		
	
	def _getModelVarsWithoutVarsKey(self):
		result = self._model.findVars()
		del result["vars"]
		
		return result
	
		
	def testFindVarsShouldContainTheVarsKey(self):
		assert("vars" in self._model.findVars().keys())
		
			
	def testFindVarsShouldReturnOnlyGetterValuesByDefault(self):		
		self.assertEquals(self._expectedVars, self._getModelVarsWithoutVarsKey())
		
	
	def testFindVarsShouldReturnSetVarsToo(self):
		self._model.setVar("omega", 27)
				
		self._expectedVars["omega"] = 27
		
		self.assertEquals(self._expectedVars, self._getModelVarsWithoutVarsKey())
		
	
	def testFindVarsShouldReturnSetVarsInsteadOfHomonymousGetterVars(self):
		self._model.setVar("alpha", 432)			
				
		self._expectedVars["alpha"] = 432
		
		self.assertEquals(self._expectedVars, self._getModelVarsWithoutVarsKey())
		
	
	def testFindVarsShouldCacheVarsWhenRequestedToTheConstructor(self):
		model = Model()
		model.setVar("ro", 50)
		model.setVar("sigma", 10)
		
		
		self.assertEquals(3, len(model.findVars()))
		
		del model._vars["ro"]
		del model._vars["vars"]
		
		self.assertEquals(["sigma"], model.findVars().keys())
		
		
		
class ViewTests(unittest.TestCase):
	def setUp(self):
		self._view = View(91)
		
	
	def testTheModelShouldBeAvailable(self):
		self.assertEquals(91, self._view._model) 			



class TemplateViewTests(ViewTests):
	def setUp(self):
		super(TemplateViewTests, self).setUp()
		self._view = TemplateView(91, "MyTemplatePath")
		
		
	def testModelAvailability(self):
		self.assertEquals(91, self._view._model) 	
		
	
	def testTemplatePathAvailability(self):
		self.assertEquals("MyTemplatePath", self._view._templatePath)