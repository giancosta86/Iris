#!/usr/bin/env python3

"""
Utility script employing HeaderRemover

:copyright: Copyright (C) 2013-2017 Gianluca Costa.
:license: LGPLv3, see LICENSE for details.
"""


import os
import sys
import re

from info.gianlucacosta.iris.io.filetree import HeaderRemover, DefaultOnProcessingFunctions


class Program:
    def _printUsage(self):
        print("Arguments: <root dir> <file path regex> <trailing regex>")
        sys.exit(1)


    def run(self, args):
        if len(args) < 3:
            self._printUsage()

        rootDir = args[0]

        if not os.path.isdir(rootDir):
            self._printUsage()

        filePathPattern = re.compile(args[1])
        trailingPattern = re.compile(args[2])

        headerRemover = HeaderRemover(filePathPattern, trailingPattern)
        headerRemover.onProcessing = DefaultOnProcessingFunctions.printProcessedFile
        headerRemover.applyTo(rootDir)


if __name__ == "__main__":
    Program().run(sys.argv[1:])
