"""
Rendering-oriented utilities

:copyright: Copyright (C) 2013-2017 Gianluca Costa.
:license: LGPLv3, see LICENSE for details.
"""

import re


class Model:
    """
    A generic model, especially dedicated to rendering.

    It is, of course, independent of the specific
    templating technology.
    """
    _getterPattern = re.compile("^(?:get|is)([A-Z]+.*)$")

    def __init__(self, cacheVars=True):
        """
        Creates the model.

        If "cacheVars" is true, the first call to findVars()
        caches the model's variables, so that no further processing
        is performed by subsequent calls.
        """
        self._vars = None
        self._explicitVars = {}
        self._cacheVars = cacheVars


    def setVar(self, name, value):
        """
        Sets a variable in the model
        """
        self._explicitVars[name] = value


    def findVars(self):
        """
        Returns the dict of model variables, as follows:

        --each getProperty() and isProperty() getter method
          is called, and a "property" key is added to the result

        --variables set via setVar() are added to the result,
          overwriting any value already provided by a getter

        The variables can be cached, to avoid further processing,
        by setting the related constructor parameter: in this case,
        findVars() returns a copy of the cached vars dictionary.
        """
        if self._cacheVars and (self._vars is not None):
            return dict(self._vars)

        result = {}

        for itemName in map(str, dir(self)):
            match = self._getterPattern.match(itemName)

            if match is None:
                continue

            propertyName = match.group(1)
            varName = propertyName[0].lower() + propertyName[1:]

            varValue = getattr(self, itemName)()

            result[varName] = varValue

        result.update(self._explicitVars)

        result["vars"] = result

        if self._cacheVars:
            self._vars = dict(result)

        return result


class View:
    """
    A generic view in a rendering system, used
    to actively create content on the basis of a model.
    """

    def __init__(self, model):
        assert (model is not None)

        self._model = model


class TemplateView(View):
    """
    A view based on a template - which can be provided, for example,
    by a templating engine.
    """

    def __init__(self, model, templatePath):
        super(TemplateView, self).__init__(model)

        assert (templatePath is not None)
        self._templatePath = templatePath
