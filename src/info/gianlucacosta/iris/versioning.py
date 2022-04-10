"""
Version management

:copyright: Copyright (C) 2013-2017 Gianluca Costa.
:license: LGPLv3, see LICENSE for details.
"""

import os


class InvalidVersionException(Exception):
    """
    Raised when an invalid version is found
    """

    def __init__(self, message):
        super(InvalidVersionException, self).__init__(message)


class Version:
    """
    Encapsulates a version, composed by the tuple:

        (major, minor, build, revision).

    Each component can be retrieved individually or as
    an integer value (which defaults to 0).

    There are 2 string representations:

    --repr() returns the version as provided to the constructor
    --str() returns a version string as returned by getFriendlyString()

    Versions are compared on their friendly string representations.
    """

    def __init__(self, source):
        """
        Creates a Version, from another Version object or from a string.
        If the string format is invalid, an exception is thrown.
        """
        if isinstance(source, Version):
            self._rawString = source._rawString
            self._major, self._minor, self._build, self._revision = source._major, source._minor, source._build, source._revision
        else:
            self._rawString = str(source)

            components = self._rawString.split(".")

            componentsLen = len(components)
            if componentsLen < 1 or componentsLen > 4:
                raise InvalidVersionException("Invalid number of version components")

            components.extend([None] * (4 - componentsLen))

            try:
                components = [int(component) if component is not None else None
                              for component in components]

                self._major, self._minor, self._build, self._revision = components
            except ValueError:
                raise InvalidVersionException("All the declared version components must be numeric")

        self._friendlyString = None


    def getMajor(self):
        return self._major

    def getIntMajor(self):
        return self._major if self._major is not None else 0

    def getMinor(self):
        return self._minor

    def getIntMinor(self):
        return self._minor if self._minor is not None else 0

    def getBuild(self):
        return self._build

    def getIntBuild(self):
        return self._build if self._build is not None else 0

    def getRevision(self):
        return self._revision

    def getIntRevision(self):
        return self._revision if self._revision is not None else 0


    def __lt__(self, other):
        if not isinstance(other, Version):
            other = Version(other)

        return str(self) < str(other)


    def __eq__(self, other):
        if not isinstance(other, Version):
            other = Version(other)

        return str(self) == str(other)


    def __hash__(self):
        return hash(self._major)


    def getRawString(self):
        """
        Returns the version string passed to the constructor
        """
        return self._rawString


    def getFriendlyString(self):
        """
        Returns the version, printed in a friendly way.

        More precisely, it trims trailing zero components.
        """
        if self._friendlyString is not None:
            return self._friendlyString

        resultComponents = [
            self.getIntMajor(),
            self.getIntMinor(),
            self.getIntBuild(),
            self.getIntRevision()
        ]

        for i in range(len(resultComponents) - 1, -1, -1):
            if resultComponents[i] == 0:
                del resultComponents[i]
            else:
                break

        result = ".".join(map(str, resultComponents))

        self._friendlyString = result

        return result


    def __repr__(self):
        return self.getRawString()


    def __str__(self):
        return self.getFriendlyString()


class VersionDirectory:
    """
    A directory whose entry names (not necessarily all)
    are valid version numbers
    """

    def __init__(self, path):
        """
        The path of the directory
        """
        self._path = path


    def getVersions(self):
        """
        Returns the versions of the suitable entries
        available in the directory - an empty list
        if no such entry is available
        """
        if not os.path.exists(self._path):
            return []

        result = []

        for entryName in os.listdir(self._path):
            try:
                entryVersion = Version(entryName)
                result.append(entryVersion)
            except InvalidVersionException:
                continue

        return result


    def getLatestVersion(self):
        """
        Returns the most recent version available in the
        directory, or None if no version entry is available
        """
        versions = self.getVersions()

        if len(versions) == 0:
            return None

        versions.sort()
        return versions[-1]
