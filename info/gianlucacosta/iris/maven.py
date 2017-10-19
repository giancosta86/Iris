"""
Maven utilities

:copyright: Copyright (C) 2013-2017 Gianluca Costa.
:license: LGPLv3, see LICENSE for details.
"""
import os

from .versioning import Version, VersionDirectory


class MavenArtifact:
    """
    A Maven artifact, identified by some common attributes
    """

    def __init__(
            self,
            groupId,
            artifactId=None,
            version=None,
            description=None,
            scope=None
    ):
        assert (groupId is not None)

        self._groupId = groupId
        self._artifactId = artifactId
        self._version = Version(version) if version is not None else None
        self._description = description
        self._scope = scope


    def getGroupId(self):
        return self._groupId

    def getArtifactId(self):
        return self._artifactId

    def getVersion(self):
        return self._version

    def getDescription(self):
        return self._description

    def getScope(self):
        return self._scope


    def getFileName(self, suffix=None, extension="jar"):
        """
        Returns the basename of the artifact's file, using Maven's conventions.

        In particular, it will be:

            <artifactId>-<version>[-<suffix>][.<extension>]
        """

        assert (self._artifactId is not None)
        assert (self._version is not None)

        return "{0}-{1}{2}{3}".format(
            self._artifactId,
            self._version.getRawString(),
            "-" + suffix.lstrip("-") if suffix is not None else "",
            "." + extension.lstrip(".") if extension is not None else ""
        )


    def getPath(self, suffix=None, extension="jar", separator=os.sep):
        """
        Returns the full path, relative to the root of a Maven repository,
        of the current artifact, using Maven's conventions.

        In particular, it will be:

            <groupId with "." replaced by <separator>>[<separator><artifactId><separator>[<version><separator><basename obtained via getFileName()>]]

        By default, <separator>=os.sep
        """

        assert (self._groupId is not None)

        resultComponents = [
            self._groupId.replace(".", separator)
        ]

        if self._artifactId is not None:
            resultComponents.append(self._artifactId)

            version = self._version
            if version is not None:
                resultComponents.append(version.getRawString())
                resultComponents.append(self.getFileName(suffix, extension))

        return separator.join(resultComponents)


    def __str__(self):
        """
        An artifact can be shown as a string only if its POM coordinates
        were all provided
        """
        assert (self._artifactId is not None)
        assert (self._version is not None)

        return "{0}:{1}:{2}".format(
            self._groupId,
            self._artifactId,
            self._version.getRawString()
        )


class MavenRepository:
    """
    A Maven repository
    """

    def __init__(self, rootPath):
        """
        Initializes the repository.

        --rootPath: the path of the repository itself
        """

        self._rootPath = rootPath


    def getRootPath(self):
        """
        Returns the root path of the repository
        """
        return self._rootPath


    def getArtifactPath(self, artifact, suffix=None, extension="jar"):
        """
        Joins the root path of the repository with the relative path returned
        by the artifact's getPath() method
        """
        return os.path.join(self._rootPath, artifact.getPath(suffix, extension, os.sep))


    def getLatestArtifactVersion(self, groupId, artifactId):
        """
        Returns the latest version of the given artifact,
        given its groupId and its artifactId.

        Returns None if no version is available for that artifact.
        """
        artifact = MavenArtifact(groupId, artifactId)

        artifactPath = self.getArtifactPath(artifact)

        artifactVersionDirectory = VersionDirectory(artifactPath)

        return artifactVersionDirectory.getLatestVersion()
