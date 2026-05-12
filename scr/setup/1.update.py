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
# FUNCTIONS
#-------------------------------------------------------------------
def cleanup() -> None:
    printHead("Cleanup ...")

def update() -> None:
    printHead("Update System ...")
    run("apt update")

def upgrade() -> None:
    printHead("Upgrade System ...")
    run("apt full-upgrade -y")

def aptPackages() -> None:
    printHead("Install APT Packages ...")
    pkgs = getList(Path("./config/apt-packages.cfg"))
    installAPT(pkgs)

def pipPackages() -> None:
    printHead("Install PIP Packages ...")
    pkgs = getList(Path("./config/pip-packages.cfg"))
    installPIP(pkgs)

#-------------------------------------------------------------------
# PROCESS
#-------------------------------------------------------------------
if __name__ == "__main__":
    try:
        checkRoot()
        checkPython()
        checkUbuntu()
        run("clear")
        update()
        run("clear")
        upgrade()
        run("clear")
        if getData("[cyan]Install APT Packages?[/cyan] (Y/n): ").lower() != 'n':
            aptPackages()
        run("clear")
        if getData("[cyan]Install PIP Packages?[/cyan] (Y/n): ").lower() != 'n':
            pipPackages()
        cleanup()
    except Exception as e:
        outlog.logError(f"Problem encountered during update: {e}")
        raise e

