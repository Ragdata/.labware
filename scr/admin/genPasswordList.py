#!/usr/bin/env python3
"""
====================================================================
Package: labware
====================================================================
Author:			Ragdata
Date:			12/05/2026
License:		MIT License
Repository:		https://github.com/Ragdata/.labware
Copyright:		Copyright © 2026 Redeyed Technologies
====================================================================
"""
import sys, tempfile, argparse

sys.path.append('../setup/mod')

from labware.filesys import *

#-------------------------------------------------------------------
# VARIABLES
#-------------------------------------------------------------------
BASEDIR = Path(config.get("paths", "base"))
WAREDIR = Path.home() / ".labware"
REPOSCR = BASEDIR / "scr/admin"

#-------------------------------------------------------------------
# PROCESS
#-------------------------------------------------------------------
if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("-f", "--file", dest="file", nargs="?", default="")

        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)

    except Exception as e:
        outlog.logError(f"Script encountered an error: {e}")
        raise e
