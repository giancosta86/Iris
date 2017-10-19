"""
:copyright: Copyright (C) 2013-2017 Gianluca Costa.
:license: LGPLv3, see LICENSE for details.
"""

import os
import shutil

from info.gianlucacosta.iris.io.utils import PathOperations

from . import AbstractIoTestCase


class PathOperationsTests(AbstractIoTestCase):
    def testSafeMakeDirsWhenPathDoesNotExist(self):
        pathToCreate = os.path.join(self._tempTestPath, "alpha", "beta", "gamma")

        assert (PathOperations.safeMakeDirs(pathToCreate))

        assert (os.path.isdir(pathToCreate))


    def testSafeMakeDirsWhenPathExists(self):
        pathToCreate = os.path.join(self._tempTestPath, "alpha", "beta", "gamma")

        PathOperations.safeMakeDirs(pathToCreate)

        self.assertFalse(PathOperations.safeMakeDirs(pathToCreate))


    def testTouchWhenIntermediateDirsDoNotExist(self):
        pathToCreate = os.path.join(self._tempTestPath, "alpha", "beta", "gamma")

        PathOperations.touch(pathToCreate)

        assert (os.path.isfile(pathToCreate))


    def testTouchWhenTheFileAlreadyExists(self):
        pathToCreate = os.path.join(self._tempTestPath, "alpha", "beta", "gamma")

        PathOperations.touch(pathToCreate)
        PathOperations.touch(pathToCreate)


    def testSafeRemoveWhenThePathExists(self):
        pathToRemove = os.path.join(self._tempTestPath, "alpha", "beta", "gamma")

        PathOperations.touch(pathToRemove)

        assert (PathOperations.safeRemove(pathToRemove))


    def testSafeRemoveWhenThePathDoesNotExist(self):
        pathToRemove = os.path.join(self._tempTestPath, "alpha", "beta", "gamma")

        self.assertFalse(PathOperations.safeRemove(pathToRemove))


    def testLinearWalkWithoutFilter(self):
        treeDir = os.path.join(self._ioTestPath, "tree")

        linearSequence = {
            os.path.join(item.dirPath, item.baseName)
            for item in PathOperations.linearWalk(treeDir)
        }

        self.assertEquals({
            os.path.join(treeDir, "sigma"),
            os.path.join(treeDir, "alpha", "T1"),
            os.path.join(treeDir, "alpha", "gamma", "delta", "T2"),
            os.path.join(treeDir, "beta", "T3")
        }, linearSequence)


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

        assert (os.path.isdir(tempTreePath))

        assert (PathOperations.safeRmTree(tempTreePath))

        assert (not os.path.isdir(tempTreePath))


    def testSafeRmTreeOnInexistentTree(self):
        tempTreePath = os.path.join(self._tempTestPath, "INEXISTENT_TREE")

        assert (not os.path.isdir(tempTreePath))
        assert (PathOperations.safeRmTree(tempTreePath))