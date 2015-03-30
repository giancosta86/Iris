# -*- coding: utf-8 -*-

"""
:copyright: Copyright (C) 2013 Gianluca Costa.
:license: LGPLv3, see LICENSE for details.
"""

from __future__ import unicode_literals

import unittest
import os
import shutil

from ..io import PathOperations, FileUtils


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


class PathOperationsTests(AbstractIoTestCase):
	def testSafeMakeDirsWhenPathDoesNotExist(self):
		pathToCreate = os.path.join(self._tempTestPath, "alpha", "beta", "gamma")
		
		assert(PathOperations.safeMakeDirs(pathToCreate))
				
		assert(os.path.isdir(pathToCreate))
		
	
	def testSafeMakeDirsWhenPathExists(self):
		pathToCreate = os.path.join(self._tempTestPath, "alpha", "beta", "gamma")
		
		PathOperations.safeMakeDirs(pathToCreate)
		
		self.assertFalse(PathOperations.safeMakeDirs(pathToCreate))
		
	
	def testTouchWhenIntermediateDirsDoNotExist(self):
		pathToCreate = os.path.join(self._tempTestPath, "alpha", "beta", "gamma")
		
		PathOperations.touch(pathToCreate)
		
		assert(os.path.isfile(pathToCreate))
		
	
	def testTouchWhenTheFileAlreadyExists(self):
		pathToCreate = os.path.join(self._tempTestPath, "alpha", "beta", "gamma")
		
		PathOperations.touch(pathToCreate)
		PathOperations.touch(pathToCreate)
		
	
	def testSafeRemoveWhenThePathExists(self):
		pathToRemove = os.path.join(self._tempTestPath, "alpha", "beta", "gamma")
		
		PathOperations.touch(pathToRemove)
		
		assert(PathOperations.safeRemove(pathToRemove))
		
	
	def testSafeRemoveWhenThePathDoesNotExist(self):
		pathToRemove = os.path.join(self._tempTestPath, "alpha", "beta", "gamma")
		
		self.assertFalse(PathOperations.safeRemove(pathToRemove))
		
		
	def testLinearWalkWithoutFilter(self):
		treeDir = os.path.join(self._ioTestPath, "tree")
		
		linearSequence = [
						os.path.join(item.dirPath, item.baseName) 
						for item in PathOperations.linearWalk(treeDir)
		]			
					
		self.assertEquals([
			os.path.join(treeDir, "sigma"),
			os.path.join(treeDir, "alpha", "T1"),
			os.path.join(treeDir, "alpha", "gamma", "delta", "T2"),
			os.path.join(treeDir, "beta", "T3")		
		], linearSequence)
		
		
	def _filterOutAlphaDirsOnly(self, dirPath, dirNames, fileNames):
		treeDir = os.path.join(self._ioTestPath, "tree")
		
		if dirPath == treeDir:
			dirNames.remove("alpha")
			
		return True
	
		
		
	def testLinearWalkUsingFilterOnDirNamesOnly(self):		
		treeDir = os.path.join(self._ioTestPath, "tree")
		
		linearSequence = [
						os.path.join(item.dirPath, item.baseName) 
						for item in PathOperations.linearWalk(treeDir, self._filterOutAlphaDirsOnly)
		]			
					
		self.assertEquals([			
			os.path.join(treeDir, "sigma"),
			os.path.join(treeDir, "beta", "T3")
		], linearSequence)
		
		
		
	def _filterOutAlphaDirsAndTheirParent(self, dirPath, dirNames, fileNames):
		treeDir = os.path.join(self._ioTestPath, "tree")
		
		if dirPath == treeDir:
			dirNames.remove("alpha")
			return False
			
			
		return True
		
	def testLinearWalkUsingFilterOnDirNamesAndParentDir(self):		
		treeDir = os.path.join(self._ioTestPath, "tree")
		
		linearSequence = [
						os.path.join(item.dirPath, item.baseName) 
						for item in PathOperations.linearWalk(treeDir, self._filterOutAlphaDirsAndTheirParent)
		]			
					
		self.assertEquals([						
			os.path.join(treeDir, "beta", "T3")
		], linearSequence)
		
	
	def testLinearWalkFilteringOnFileNames(self):
		treeDir = os.path.join(self._ioTestPath, "tree")
		
		linearSequence = [
						os.path.join(item.dirPath, item.baseName) 
						for item in PathOperations.linearWalk(
							treeDir, 
							lambda dirPath, dirNames, fileNames: "T2" in fileNames
						)
		]			
					
		self.assertEquals([	
			os.path.join(treeDir, "alpha", "gamma", "delta", "T2")
		], linearSequence)
		
	
	def testSafeRmTreeWhenDeletingExistingTree(self):
		tempTreePath = os.path.join(self._tempTestPath, "tree")
		
		shutil.copytree(
			os.path.join(self._ioTestPath, "tree"),
			tempTreePath
		)		
		
		assert(os.path.isdir(tempTreePath))
		
		assert(PathOperations.safeRmTree(tempTreePath))
		
		assert(not os.path.isdir(tempTreePath))
		
	
	
	def testSafeRmTreeOnInexistingTree(self):
		tempTreePath = os.path.join(self._tempTestPath, "INEXISTING_TREE")			
		
		assert(not os.path.isdir(tempTreePath))
		assert(PathOperations.safeRmTree(tempTreePath))

	

class FileUtilsTests(AbstractIoTestCase):
	def testOpenEncodedUsingUtf8(self):
		unicodeString = "àèìòù"
				
		filePath = os.path.join(self._tempTestPath, "encodingTest")
		
		with FileUtils.openEncoded(filePath, "w") as utf8File:
			utf8File.write(unicodeString)
		
		with FileUtils.openEncoded(filePath, "r") as utf8File:
			retrievedString = utf8File.read()
			
		self.assertEquals(unicodeString, retrievedString)
		
		
	def testOpenEncodedSavingUnicodeToAscii(self):
		unicodeString = "àèìòù"
				
		filePath = os.path.join(self._tempTestPath, "encodingTest")
		
		with FileUtils.openEncoded(filePath, "w", encoding="ascii") as asciiFile:
			self.assertRaises(UnicodeEncodeError, asciiFile.write, unicodeString)
		
	