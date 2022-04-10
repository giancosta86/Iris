"""
:copyright: Copyright (C) 2013-2017 Gianluca Costa.
:license: LGPLv3, see LICENSE for details.
"""


import unittest
import os
import shutil


class AbstractIoTestCase(unittest.TestCase):
    def setUp(self):
        self._ioTestPath = os.path.dirname(__file__)

        self._tempTestPath = os.path.join(
            self._ioTestPath,
            "transientTests"
        )

        os.makedirs(self._tempTestPath)


    def tearDown(self):
        if os.path.exists(self._tempTestPath):
            shutil.rmtree(self._tempTestPath)
