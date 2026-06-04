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

sys.path.append(".")

from labware.filesys import *

from scr.setup.sec import banner

#-------------------------------------------------------------------
# PROCESS
#-------------------------------------------------------------------
def execute():
    try:
        clear()
        banner.execute()
        rule(f"[yellow]── CIS BENCHMARKING LEVEL 1 SERVER HARDENING - TOOLS MODULE [/yellow]", style="yellow", align="left")
        line()
        # ----------------------------------------------------------
        # INSTALL BASIC TOOLS
        # ----------------------------------------------------------
        printHead("Installing Basic Tools ...")
        basic = Path(config.get("paths", "setup")) / "cfg" / "apt-basic.cfg"
        if not basic.exists():
            raise FileNotFoundError(f"File not found: '{basic}'")
        pkgs = getList(basic)
        installAPT(pkgs)
        # ----------------------------------------------------------
        # INSTALL SECURITY TOOLS
        # ----------------------------------------------------------
        clear()
        banner.execute()
        rule(f"[yellow]── TOOLS MODULE [/yellow]", style="yellow", align="left")
        line()
        printHead("Installing Security Tools ...")
        secure = Path(config.get("paths", "setup")) / "cfg" / "apt-secure.cfg"
        if not secure.exists():
            raise FileNotFoundError(f"File not found: '{secure}'")
        pkgs = getList(secure)
        installAPT(pkgs)
        # ----------------------------------------------------------
        # INSTALL PRIMARY TOOLS
        # ----------------------------------------------------------
        clear()
        banner.execute()
        rule(f"[yellow]── TOOLS MODULE [/yellow]", style="yellow", align="left")
        line()
        printHead("Installing Primary Packages ...")
        webmin = getData("[cyan]Install Webmin?[/cyan] (Y/n): ").lower()
        if webmin != 'n':
            path = Path(config.get("paths", "scripts")) / "webmin.py"
            runpy.run_path(str(path))
        else:
            virtualmin = getData("[cyan]Install Virtualmin[/cyan] (Y/n): ").lower()
            if virtualmin != 'n':
                path = Path(config.get("paths", "scripts")) / "virtualmin.py"
                runpy.run_path(str(path))
        docker = getData("[cyan]Install Docker[/cyan] (Y/n): ").lower()
        if docker != 'n':
            path = Path(config.get("paths", "scripts")) / "docker.py"
            runpy.run_path(str(path))
        lazydocker = getData("[cyan]Install LazyDocker[/cyan] (Y/n): ").lower()
        if lazydocker != 'n':
            path = Path(config.get("paths", "scripts")) / "lazydocker.py"
            runpy.run_path(str(path))
    except Exception as e:
        logger.error(f"An error occurred: {e}", True)
        raise

# ===========================================================================
# ENTRY POINT
# ===========================================================================
if __name__ == "__main__":
    execute()
