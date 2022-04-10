"""
:copyright: Copyright (C) 2013-2017 Gianluca Costa.
:license: LGPLv3, see LICENSE for details.
"""

import os
import shutil

from info.gianlucacosta.iris.io.filetree import HeaderRemover, TrailingSpaceRemover

from . import AbstractIoTestCase


class FileTreeTestCase(AbstractIoTestCase):
    def setUp(self):
        super().setUp()

        self._tempFileTreePath = os.path.join(self._tempTestPath, "filetree")

        shutil.copytree(
            os.path.join(self._ioTestPath, "filetree"),
            self._tempFileTreePath
        )



class HeaderRemoverTests(FileTreeTestCase):
    def setUp(self):
        super().setUp()

        self._headerRemover = HeaderRemover(
            r".*\.(java|cs|js|c|cpp)$",
            r"(?s)^.*==========================%##\s+\*/[\r\n]+"
        )

    def testApplyTo_WithJavaFile(self):
        self._headerRemover.applyTo(self._tempFileTreePath)

        with open(os.path.join(self._tempFileTreePath, "alpha", "beta", "lambda.java"), "r") as sourceFile:
            lines = sourceFile.readlines()

        expectedLines = [
            "package test;\n",
            "\n",
            "class Hello {}\n",
        ]

        self.assertListEqual(expectedLines, lines)


    def testApplyTo_WithPlainTextFile(self):
        self._headerRemover.applyTo(self._tempFileTreePath)

        with open(os.path.join(self._tempFileTreePath, "alpha", "beta", "mi.txt"), "r") as sourceFile:
            lines = sourceFile.readlines()


        expectedLines = [
            "/*=================\n",
            "In a text file nothing must be deleted\n",
            "================================%##\n",
            "*/\n",
            "hi\n"
        ]


        self.assertListEqual(expectedLines, lines)


    def testApplyTo_WithJavaFileHavingNoHeader(self):
        self._headerRemover.applyTo(self._tempFileTreePath)

        with open(os.path.join(self._tempFileTreePath, "alpha", "beta", "ni.java"), "r") as sourceFile:
            lines = sourceFile.readlines()

        expectedLines = [
            "package test;\n",
            "\n",
            "class Hello2 {}\n",
        ]

        self.assertListEqual(expectedLines, lines)



class TrailingSpaceRemoverTests(FileTreeTestCase):
    def setUp(self):
        super().setUp()

        self._trailingSpaceRemover = TrailingSpaceRemover(
            r".*\.(java|cs|js|c|cpp)$"
        )

    def testApplyTo_WithJavaFile(self):
        self._trailingSpaceRemover.applyTo(self._tempFileTreePath)

        with open(os.path.join(self._tempFileTreePath, "gamma", "spaces.java"), "r") as sourceFile:
            processedLines = sourceFile.readlines()


        expectedLines = [
           "This file\n",
            "\n",
            "\n",
            "   has indeed\n",
            "\n",
            "        quite a lot of trailing spaces! ^__^!\n",
           "\n"
        ]


        self.assertListEqual(expectedLines, processedLines)


    def testApplyTo_WithPlainTextFile(self):
        self._trailingSpaceRemover.applyTo(self._tempFileTreePath)

        with open(os.path.join(self._tempFileTreePath, "gamma", "spaces.txt"), "r") as sourceFile:
            processedLines = sourceFile.readlines()


        expectedLines = [
           "This file      \n",
            "\n",
            "\n",
            "   has indeed		\n",
            "\n",
            "        quite a lot of trailing spaces! ^__^!\n",
           "\n"
        ]


        self.assertListEqual(expectedLines, processedLines)