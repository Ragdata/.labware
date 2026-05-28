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
import sys, runpy

sys.path.append("../mod")

from mod.filesys import *

#-------------------------------------------------------------------
# PROCESS
#-------------------------------------------------------------------
if __name__ == "__main__":
    try:
        # ----------------------------------------------------------
        # INSTALL BASIC TOOLS
        # ----------------------------------------------------------
        line()
        printHead("Installing Basic Tools ...")
        basic = BASEDIR / "src/setup/cfg/apt-basic.cfg"
        if not basic.exists():
            raise FileNotFoundError(f"File not found: '{basic}'")
        pkgs = getList(basic)
        installAPT(pkgs)
        # ----------------------------------------------------------
        # INSTALL SECURITY TOOLS
        # ----------------------------------------------------------
        line()
        printHead("Installing Security Tools ...")
        secure = BASEDIR / "src/setup/cfg/apt-secure.cfg"
        if not secure.exists():
            raise FileNotFoundError(f"File not found: '{secure}'")
        pkgs = getList(secure)
        installAPT(pkgs)
        # ----------------------------------------------------------
        # INSTALL PRIMARY TOOLS
        # ----------------------------------------------------------
        line()
        printHead("Installing Primary Packages ...")
        webmin = getData("[cyan]Install Webmin?[/cyan] (Y/n): ").lower()
        if webmin != 'n':
            runpy.run_path("pkg/webmin.py")
        else:
            virtualmin = getData("[cyan]Install Virtualmin[/cyan] (Y/n): ").lower()
            if virtualmin != 'n':
                runpy.run_path("pkg/virtualmin.py")
        docker = getData("[cyan]Install Docker[/cyan] (Y/n): ").lower()
        if docker != 'n':
            runpy.run_path("pkg/docker.py")
        lazydocker = getData("[cyan]Install LazyDocker[/cyan] (Y/n): ").lower()
        if lazydocker != 'n':
            runpy.run_path("pkg/lazydocker.py")
    except Exception as e:
        outlog.logError(f"An error occurred in sec.tools.py: {e}")
        raise e
