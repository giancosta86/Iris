#!/usr/bin/env python3

"""
Utility script employing TrailingSpaceRemover

:copyright: Copyright (C) 2013-2017 Gianluca Costa.
:license: LGPLv3, see LICENSE for details.
"""


import sys
import re

from info.gianlucacosta.iris.io.filetree import TrailingSpaceRemover, DefaultOnProcessingFunctions


class Program:
    def run(self, args):
        rootDir = args[0]
        filePathRegex = args[1]

        trailingSpaceRemover = TrailingSpaceRemover(re.compile(filePathRegex))
        trailingSpaceRemover.onProcessing = DefaultOnProcessingFunctions.printProcessedFile
        trailingSpaceRemover.applyTo(rootDir)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Arguments: <root dir> [<file path regex>]")
        sys.exit(1)

    elif len(sys.argv) < 3:
        sys.argv.append(r".*\.(java|htm|html|xml|cs|py|js|c|cpp)$")

    Program().run(sys.argv[1:])
