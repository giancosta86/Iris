# -*- coding: utf-8 -*-

"""
:copyright: Copyright (C) 2013 Gianluca Costa.
:license: LGPLv3, see LICENSE for details.
"""

from __future__ import unicode_literals

import unittest
import os
import shutil
import sys

from ..web import SiteInfoService


class AbstractSiteTestCase(unittest.TestCase):
	def setUp(self):
		self._scriptDirPath = os.path.normpath(os.path.dirname(sys.argv[0]))
		self._siteDirPath = os.path.join(self._scriptDirPath, "site")

		os.environ["DOCUMENT_ROOT"] = self._siteDirPath

		self._siteInfoService = SiteInfoService()
		self._deltreeSiteDir()


	def tearDown(self):
		self._deltreeSiteDir()


	def _deltreeSiteDir(self):
		if os.path.exists(self._siteDirPath):
			shutil.rmtree(self._siteDirPath)
