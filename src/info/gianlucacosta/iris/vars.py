"""
File-based management of variables.

:copyright: Copyright (C) 2013-2017 Gianluca Costa.
:license: LGPLv3, see LICENSE for details.
"""
import os

from .io.utils import PathOperations


class VariablesService:
    """
    Centralizes several file-based variables in one directory
    """

    def __init__(self, variablesDirPath):
        """
        Instantiates the service, receiving the directory that
        will contain the variable-related files
        """
        self._variablesDirPath = variablesDirPath

    def getFlag(self, flagName):
        """
        Creates a flag having path <variables dir path><os.sep><flagName>
        """
        assert (len(flagName) > 0)

        return Flag(os.path.join(self._variablesDirPath, flagName))


class Flag:
    """
    A Flag is a boolean variable whose value depends
    on the existence of the underlying path: isActive()
    returns true if and only if that path exists.

    This concept can be very handy when using different
    technologies, that use files as a simple communication
    means.
    """

    def __init__(self, path):
        self._path = path


    def getPath(self):
        return self._path


    def isActive(self):
        """
        Returns the value of the flag
        """
        return os.path.exists(self._path)


    def activate(self):
        """
        Sets the flag's value to true
        """
        PathOperations.touch(self._path)


    def deactivate(self):
        """
        Sets the flag's value to false
        """
        PathOperations.safeRemove(self._path)


    def flip(self):
        """
        Flips the state of the flag
        """
        if self.isActive():
            self.deactivate()
        else:
            self.activate()
