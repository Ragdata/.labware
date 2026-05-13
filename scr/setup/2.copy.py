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
import sys

sys.path.append('.')

from utils import *


#-------------------------------------------------------------------
# VARIABLES
#-------------------------------------------------------------------
BASEDIR = Path(config.get("paths", "base"))
USERDIR = Path.home() / '.labware'
REPOLIB = BASEDIR / 'sys' / 'lib'
REPODOT = BASEDIR / 'sys' / 'dots'
REPOETC = BASEDIR / 'sys' / 'etc'
USERLIB = USERDIR / 'lib'

#-------------------------------------------------------------------
# FUNCTIONS
#-------------------------------------------------------------------

#-------------------------------------------------------------------
# PROCESS
#-------------------------------------------------------------------
if __name__ == "__main__":
    try:
        checkRoot()
        checkPython()
        checkRoot()
        run("clear")
        # Library Files
        printHead("Installing Library Files ...")
        copyFiles(REPOLIB, USERLIB)
        # Backup DotFiles
        printHead("Backup DotFiles ...")
        if not backup(Path.home() / '.bashrc'):
            printWarning("Failed to backup '.bashrc'")
        else:
            printSuccess("Backup '.bashrc")
        if not backup(Path.home() / '.profile'):
            printWarning("Failed to backup '.profile'")
        else:
            printSuccess("Backup '.profile")
        if not backup(Path.home() / '.gitconfig'):
            printWarning("Failed to backup '.gitconfig'")
        else:
            printSuccess("Backup '.gitconfig")
        # Install DotFiles
        printHead("Installing DotFiles ...")
        copyFiles(REPODOT, Path.home())
        # Install Configs
        printHead("Installing Configs ...")
        copyFiles(REPOETC, USERDIR / 'etc')
    except Exception as e:
        outlog.logError(f"Problem encountered during file copy: {e}")
        raise e
