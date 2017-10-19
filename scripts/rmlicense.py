#!/usr/bin/env python3

"""
Utility script employing HeaderRemover to remove license headers created by Maven projects extending "jar-plus"

:copyright: Copyright (C) 2013-2017 Gianluca Costa.
:license: LGPLv3, see LICENSE for details.
"""

import sys

from rmheader import Program


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Arguments: <root dir>")
        sys.exit(1)


    # For Java
    Program().run(
        [
            sys.argv[1],
            r".*\.(java|cs|js|c|cpp)$",
            r"(?s)^.*==========================%##\s+\*/[\r\n]+"
        ]
    )

    # For HTML/XML
    Program().run(
        [
            sys.argv[1],
            r".*\.(htm|html|xml)$",
            r"(?s)^.*==========================%##\s+\-->[\r\n]+"
        ]
    )

