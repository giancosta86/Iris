"""
:copyright: Copyright (C) 2013-2017 Gianluca Costa.
:license: LGPLv3, see LICENSE for details.
"""

import os

from info.gianlucacosta.iris.vars import VariablesService, Flag
from info.gianlucacosta.iris.io.utils import PathOperations

from .io import AbstractIoTestCase


class VariablesTestCase(AbstractIoTestCase):
    def setUp(self):
        super(VariablesTestCase, self).setUp()

        self._varsDir = os.path.join(self._tempTestPath, "_vars")
        self._variablesService = VariablesService(self._varsDir)


class VariablesServiceTests(VariablesTestCase):
    def testGetFlag(self):
        flag = self._variablesService.getFlag("myTestFlag")
        assert (flag is not None)


class FlagTests(VariablesTestCase):
    def setUp(self):
        super(FlagTests, self).setUp()

        self._flagPath = os.path.join(self._varsDir, "SimpleTestFlag")

        PathOperations.safeRemove(self._flagPath)

        self._flag = Flag(self._flagPath)


    def testGetPathAfterRetrievingTheInexistentFlag(self):
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