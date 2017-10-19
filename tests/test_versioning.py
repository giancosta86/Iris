"""
:copyright: Copyright (C) 2013-2017 Gianluca Costa.
:license: LGPLv3, see LICENSE for details.
"""

import unittest
import os

from info.gianlucacosta.iris.versioning import Version, VersionDirectory, InvalidVersionException


class VersionTests(unittest.TestCase):
    def testConstructorWithFullStringParameter(self):
        version = Version("1.2.3.4")
        self.assertEquals(1, version.getMajor())
        self.assertEquals(2, version.getMinor())
        self.assertEquals(3, version.getBuild())
        self.assertEquals(4, version.getRevision())


    def testConstructorWhenTheVersionStringIsTooLong(self):
        self.assertRaises(InvalidVersionException, Version, "1.2.3.4.5")


    def testConstructorWhenTheVersionStringIsInvalid(self):
        self.assertRaises(InvalidVersionException, Version, "AnInvalidVersionString")


    def testConstructorWhenPassingAnotherVersion(self):
        version = Version("6.7.8.9")
        self.assertEquals(version, Version(version))


    def testRepr(self):
        rawString = "7.6.0"
        version = Version(rawString)
        self.assertEquals(rawString, repr(version))


    def testCastingToStringWhenOnlyTheRevisionIsNonZero(self):
        versionString = "0.0.0.4"
        version = Version(versionString)
        self.assertEquals(versionString, str(version))


    def testCastingToStringWithAlternateZeros(self):
        versionString = "0.2.0.4"
        version = Version(versionString)
        self.assertEquals(versionString, str(version))


    def testEqualityOfVersionAndString(self):
        version = Version("1.2.3.4")
        self.assertEquals(version, "1.2.3.4")


    def testEqualityOfVersionAndStringWhenThereAreTrailingZeros(self):
        version = Version("1.2")
        self.assertEquals(version, "1.2")
        self.assertEquals(version, "1.2.0")
        self.assertEquals(version, "1.2.0.0")


    def testConstructorWithOnlyMajor(self):
        version = Version("5")
        self.assertEquals(version, "5")


    def testConstructorWithMajorAndMinor(self):
        version = Version("5.6")
        self.assertEquals(version, "5.6")


    def testConstructorWithMajorMinorAndBuild(self):
        version = Version("5.6.7")
        self.assertEquals(version, "5.6.7")


    def testConstructorWithMajorMinorBuildAndRelease(self):
        version = Version("5.6.7.8")
        self.assertEquals(version, "5.6.7.8")


    def testComparisonWithMajor(self):
        laterVersion = Version("5")
        olderVersion = Version("4")

        assert (olderVersion < laterVersion)


    def testComparisonWithMinor(self):
        laterVersion = Version("5.4")
        olderVersion = Version("5.3")

        assert (olderVersion < laterVersion)


    def testComparisonWithBuild(self):
        laterVersion = Version("5.4.8")
        olderVersion = Version("5.4.7")

        assert (olderVersion < laterVersion)


    def testComparisonWithRevision(self):
        laterVersion = Version("5.4.8.3")
        olderVersion = Version("5.4.8.2")

        assert (olderVersion < laterVersion)


    def testEqualityWithMajor(self):
        firstVersion = Version("4")
        secondVersion = Version("4")

        self.assertEquals(firstVersion, secondVersion)


    def testEqualityWithMajorAndMinor(self):
        firstVersion = Version("4.5")
        secondVersion = Version("4.5")

        self.assertEquals(firstVersion, secondVersion)


    def testEqualityWithMajorMinorAndBuild(self):
        firstVersion = Version("4.5.6")
        secondVersion = Version("4.5.6")

        self.assertEquals(firstVersion, secondVersion)


    def testEqualityWithMajorMinorBuildAndRelease(self):
        firstVersion = Version("4.5.6.7")
        secondVersion = Version("4.5.6.7")

        self.assertEquals(firstVersion, secondVersion)


class VersionDirectoryTests(unittest.TestCase):
    def setUp(self):
        self._versionDirectory = VersionDirectory(os.path.join(os.path.dirname(__file__), "versions"))
        self._inexistentVersionDirectory = VersionDirectory(
            os.path.join(os.path.dirname(__file__), "INEXISTENT_VERSION_DIR"))


    def testGetVersions(self):
        versions = self._versionDirectory.getVersions()
        versions.sort()

        self.assertEquals([Version("2"), Version("3.5.6.7"), Version("4.8"), Version("6.1.2")], versions)


    def testGetVersionsOnAnInexistentDirectory(self):
        versions = self._inexistentVersionDirectory.getVersions()

        self.assertEquals([], versions)


    def testGetLatestVersion(self):
        latestVersion = self._versionDirectory.getLatestVersion()

        self.assertEquals(Version("6.1.2"), latestVersion)


    def testGetLatestVersionOnAnInexistentDirectory(self):
        latestVersion = self._inexistentVersionDirectory.getLatestVersion()

        self.assertIsNone(latestVersion)