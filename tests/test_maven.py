"""
:copyright: Copyright (C) 2013-2022 Gianluca Costa.
:license: LGPLv3, see LICENSE for details.
"""

import unittest
import os

from info.gianlucacosta.iris.maven import MavenArtifact, MavenRepository


class MavenArtifactTests(unittest.TestCase):
    def setUp(self):
        self._fullArtifact = MavenArtifact("psi.tau", "alpha.beta", "4.5")

    def testConstructor(self):
        groupId = "myGroup"
        artifactId = "myArtifact"
        versionString = "8.10"
        description = "My description"
        scope = "My scope"

        artifact = MavenArtifact(groupId, artifactId, versionString, description, scope)
        self.assertEqual(groupId, artifact.getGroupId())
        self.assertEqual(artifactId, artifact.getArtifactId())
        self.assertEqual(versionString, artifact.getVersion())
        self.assertEqual(description, artifact.getDescription())
        self.assertEqual(scope, artifact.getScope())

    def testGetFileNameWithBasicArtifact(self):
        self.assertEqual("alpha.beta-4.5.jar", self._fullArtifact.getFileName())

    def testGetFileNameWithSuffix(self):
        self.assertEqual(
            "alpha.beta-4.5-javadoc.jar", self._fullArtifact.getFileName("javadoc")
        )

    def testGetFileNameWithSuffixHavingLeadingDash(self):
        self.assertEqual(
            "alpha.beta-4.5-javadoc.jar", self._fullArtifact.getFileName("-javadoc")
        )

    def testGetFileNameWithExtension(self):
        self.assertEqual(
            "alpha.beta-4.5.nbm", self._fullArtifact.getFileName(extension="nbm")
        )

    def testGetFileNameWithExtensionHavingLeadingDot(self):
        self.assertEqual(
            "alpha.beta-4.5.nbm", self._fullArtifact.getFileName(extension=".nbm")
        )

    def testGetFileNameWithSuffixAndExtension(self):
        self.assertEqual(
            "alpha.beta-4.5-javadoc.nbm",
            self._fullArtifact.getFileName("javadoc", "nbm"),
        )

    def testGetPathWithGroupIdOnly(self):
        artifact = MavenArtifact("psi.tau")
        self.assertEqual("psi{0}tau".format(os.sep), artifact.getPath())

    def testGetPathWithGroupIdAndArtifactId(self):
        artifact = MavenArtifact("psi.tau", "alpha.beta")
        self.assertEqual("psi{0}tau{0}alpha.beta".format(os.sep), artifact.getPath())

    def testGetPathWithFullArtifact(self):
        artifact = self._fullArtifact
        self.assertEqual(
            "psi{0}tau{0}alpha.beta{0}4.5{0}alpha.beta-4.5.jar".format(os.sep),
            artifact.getPath(),
        )

    def testGetPathWithFullArtifactAndSuffix(self):
        artifact = self._fullArtifact
        self.assertEqual(
            "psi{0}tau{0}alpha.beta{0}4.5{0}alpha.beta-4.5-javadoc.jar".format(os.sep),
            artifact.getPath("javadoc"),
        )

    def testGetPathWithFullArtifactAndExtension(self):
        artifact = self._fullArtifact
        self.assertEqual(
            "psi{0}tau{0}alpha.beta{0}4.5{0}alpha.beta-4.5.nbm".format(os.sep),
            artifact.getPath(extension="nbm"),
        )

    def testGetPathWithFullArtifactAndSuffixAndExtension(self):
        artifact = self._fullArtifact
        self.assertEqual(
            "psi{0}tau{0}alpha.beta{0}4.5{0}alpha.beta-4.5-javadoc.nbm".format(os.sep),
            artifact.getPath("javadoc", "nbm"),
        )

    def testStr(self):
        self.assertEqual("psi.tau:alpha.beta:4.5", str(self._fullArtifact))


class MavenRepositoryTests(unittest.TestCase):
    def setUp(self):
        self._rootPath = os.path.join(os.path.dirname(__file__), "mvn")
        self._mavenRepository = MavenRepository(self._rootPath)
        self._fullArtifact = MavenArtifact("psi.tau", "alpha.beta", "4.5")

    def testGetRootPath(self):
        self.assertEqual(self._rootPath, self._mavenRepository.getRootPath())

    def testGetArtifactPathWithGroupIdOnly(self):
        artifact = MavenArtifact("psi.tau")
        artifactPath = self._mavenRepository.getArtifactPath(artifact)

        self.assertEqual(os.path.join(self._rootPath, "psi", "tau"), artifactPath)

    def testGetArtifactPathWithGroupIdAndArtifactId(self):
        artifact = MavenArtifact("psi.tau", "alpha.beta")
        artifactPath = self._mavenRepository.getArtifactPath(artifact)

        self.assertEqual(
            os.path.join(self._rootPath, "psi", "tau", "alpha.beta"), artifactPath
        )

    def testGetArtifactPathWithFullArtifact(self):
        artifact = self._fullArtifact
        artifactPath = self._mavenRepository.getArtifactPath(artifact)

        self.assertEqual(
            os.path.join(
                self._rootPath, "psi", "tau", "alpha.beta", "4.5", "alpha.beta-4.5.jar"
            ),
            artifactPath,
        )

    def testGetArtifactPathWithFullArtifactAndSuffix(self):
        artifact = self._fullArtifact
        artifactPath = self._mavenRepository.getArtifactPath(artifact, "javadoc")

        self.assertEqual(
            os.path.join(
                self._rootPath,
                "psi",
                "tau",
                "alpha.beta",
                "4.5",
                "alpha.beta-4.5-javadoc.jar",
            ),
            artifactPath,
        )

    def testGetArtifactPathWithFullArtifactAndExtension(self):
        artifact = self._fullArtifact
        artifactPath = self._mavenRepository.getArtifactPath(artifact, extension="nbm")

        self.assertEqual(
            os.path.join(
                self._rootPath, "psi", "tau", "alpha.beta", "4.5", "alpha.beta-4.5.nbm"
            ),
            artifactPath,
        )

    def testGetArtifactPathWithFullArtifactAndSuffixAndExtension(self):
        artifact = self._fullArtifact
        artifactPath = self._mavenRepository.getArtifactPath(artifact, "javadoc", "nbm")

        self.assertEqual(
            os.path.join(
                self._rootPath,
                "psi",
                "tau",
                "alpha.beta",
                "4.5",
                "alpha.beta-4.5-javadoc.nbm",
            ),
            artifactPath,
        )

    def testLatestArtifactVersion(self):
        latestVersion = self._mavenRepository.getLatestArtifactVersion(
            "test.group", "sample.artifact"
        )

        self.assertEqual("28.3", latestVersion)
