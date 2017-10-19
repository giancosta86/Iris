"""
:copyright: Copyright (C) 2013-2017 Gianluca Costa.
:license: LGPLv3, see LICENSE for details.
"""

import unittest

from info.gianlucacosta.iris.rendering import Model, View, TemplateView


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


    def testFindVars_ShouldContainTheVarsKey(self):
        assert ("vars" in self._model.findVars().keys())


    def testFindVars_ShouldReturnOnlyGetterValuesByDefault(self):
        self.assertEquals(self._expectedVars, self._getModelVarsWithoutVarsKey())


    def testFindVars_ShouldReturnSetVarsToo(self):
        self._model.setVar("omega", 27)

        self._expectedVars["omega"] = 27

        self.assertEquals(self._expectedVars, self._getModelVarsWithoutVarsKey())


    def testFindVars_ShouldReturnSetVarsInsteadOfHomonymGetterVars(self):
        self._model.setVar("alpha", 432)

        self._expectedVars["alpha"] = 432

        self.assertEquals(self._expectedVars, self._getModelVarsWithoutVarsKey())


    def testFindVars_ShouldCacheVarsWhenRequestedToTheConstructor(self):
        model = Model()
        model.setVar("ro", 50)
        model.setVar("sigma", 10)

        self.assertEquals(3, len(model.findVars()))

        del model._vars["ro"]
        del model._vars["vars"]

        self.assertEquals(["sigma"], list(model.findVars().keys()))


class ViewTests(unittest.TestCase):
    def setUp(self):
        self._view = View(91)


    def testTheModel_ShouldBeAvailable(self):
        self.assertEquals(91, self._view._model)


class TemplateViewTests(ViewTests):
    def setUp(self):
        super(TemplateViewTests, self).setUp()
        self._view = TemplateView(91, "MyTemplatePath")


    def testModelAvailability(self):
        self.assertEquals(91, self._view._model)


    def testTemplatePathAvailability(self):
        self.assertEquals("MyTemplatePath", self._view._templatePath)